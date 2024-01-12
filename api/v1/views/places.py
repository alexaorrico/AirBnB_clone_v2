#!/usr/bin/python3
"""Place view objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.state import State


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a Place
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    user = storage.get(User, request.get_json()['user_id'])
    if user is None:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    place = Place(**request.get_json())
    place.city_id = city_id
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """
    if request.get_json() is None:
        abort(400, description="Not a JSON")

    request_data = request.get_json()

    if request_data and len(request_data):
        state_ids = request_data.get('states', None)
        city_ids = request_data.get('cities', None)
        amenity_ids = request_data.get('amenities', None)

    if not request_data or not len(request_data) or (
            not state_ids and
            not city_ids and
            not amenity_ids):
        all_places = storage.all(Place).values()
        places_list = [place.to_dict() for place in all_places]
        return jsonify(places_list)

    filtered_places = []

    if state_ids:
        state_objects = [storage.get(State, state_id)
                         for state_id in state_ids]
        for state in state_objects:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            filtered_places.append(place)

    if city_ids:
        city_objects = [storage.get(City, city_id) for city_id in city_ids]
        for city in city_objects:
            if city:
                for place in city.places:
                    if place not in filtered_places:
                        filtered_places.append(place)

    if amenity_ids:
        if not filtered_places:
            filtered_places = storage.all(Place).values()
        amenity_objects = [storage.get(Amenity, amenity_id)
                           for amenity_id in amenity_ids]
        filtered_places = [place for place in filtered_places if all(
            amenity in place.amenities for amenity in amenity_objects)]

    places_to_return = []
    for place in filtered_places:
        place_dict = place.to_dict()
        place_dict.pop('amenities', None)
        places_to_return.append(place_dict)

    return jsonify(places_to_return)
