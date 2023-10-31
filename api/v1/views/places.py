#!/usr/bin/python3
"""
places view api
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
    retrieves all Place object of a City
    """
    city = storage.get(City, city_id)
    if city:
        places = []
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """
    retrieves a Place object
    """
    place = storage.get(Place, place_id)
    if place:
        response = place.to_dict()
        return jsonify(response)
    abort(404)


@app_views.route('/place/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    deletes a place object
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    create a Place object
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, "Missing user_id")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if 'name' not in data:
        abort(400, "Missing name")
    place = Place(**data)
    place.save()
    response = place.to_dict()
    return jsonify(response), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    updates a Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    data = request.get_json()
    ignore_attributes = [
        'id', 'user_id', 'city_id', 'created_at', 'updated_at'
    ]
    for attribute, value in data.items():
        if attribute not in ignore_attributes:
            setattr(place, attribute, value)
    place.save()
    response = place.to_dict()
    return jsonify(response), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """
    retrieves all Places objects depending on the body of th request
    """
    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    if not states and not cities and not amenities:
        places = []
        for place in storage.all(Place).values():
            places.append(place.to_dict())
        return jsonify(places)
    places = []

    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                for place in city.places:
                    if place.id not in [p['id'] for p in places]:
                        places.append(place.to_dict())

    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            for place in sity.places:
                if place.id not in [p['id'] for p in places]:
                    places.append(place.to_dict())

    if amenities:
        places = [place for place in places if all(amenity.id in [a.id for
                  a in place.amenities] for amenity_id in amenities)]

    return jsonify(places)
