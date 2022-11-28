#!/usr/bin/python3
"""handles default RESTful API actions for Place objects"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import abort, request, make_response, jsonify


@app_views.route('cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_city_place(city_id=None):
    """retrives all places within a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """retrieves a place from id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id=None):
    """deletes a place from its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id=None):
    """creates a place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_data = request.get_json()
    if place_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in place_data.keys():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if storage.get(User, place_data['user_id']) is None:
        abort(404)
    if 'name' not in place_data.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_place = Place(**place_data)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_data = request.get_json()
    if place_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, val in place_data.values():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, val)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
