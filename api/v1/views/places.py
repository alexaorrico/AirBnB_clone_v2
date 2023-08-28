#!/usr/bin/python3
"""states script"""

from api.v1.views import app_views
from flask import jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.user import User


@app_views.route('cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def list_all_places(city_id):
    '''Retrieves a list of all city objects of a state id'''
    city = storage.get(City, city_id)
    if city is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    list_places = [place.to_dict() for place in city.places]
    return jsonify(list_places)


@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a city object by ID"""
    place = storage.get(Place, place_id)
    if place is not None:
        return jsonify(place.to_dict())
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a city object by ID"""
    place = storage.get(Place, place_id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a new city"""
    city = storage.get(City, city_id)
    if city is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request_data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user_id = request_data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    if 'name' not in request_data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_place = Place(name=request.json['name'],
                      user_id=request.json['user_id'], city_id=city_id)
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a State object by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        return make_response(jsonify({'error': 'not found'}), 404)
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request_data.items():
        if key not in ['id', 'state_id', 'city_id', 'created_at',
                       'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
