#!/usr/bin/python3
"""Places objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.state import State


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, description="Missing name")
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Retrieves all Place objects depending on the request."""
    try:
        if not request.get_json():
            abort(400, description="Not a JSON")

        body = request.get_json()
        states = body.get('states', [])
        cities = body.get('cities', [])
        amenities = body.get('amenities', [])

        if not states and not cities and not amenities:
            places = storage.all(Place).values()
            return jsonify([place.to_dict() for place in places])

        places = set()

        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    for city in state.cities:
                        places.update(city.places)

        if cities:
            for city_id in cities:
                city = storage.get(City, city_id)
                if city:
                    places.update(city.places)

        if amenities:
            places = [
                place for place in places
                if all(
                    amenity_id in [amenity.id for amenity in place.amenities]
                    for amenity_id in amenities
                )
            ]

        return jsonify([place.to_dict() for place in places])

    except Exception as e:
        return jsonify({"error": str(e)}), 500
