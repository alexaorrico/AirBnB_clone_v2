#!/usr/bin/python3
"""states script"""

from api.v1.views import app_views
from flask import jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def list_all_cities(state_id):
    '''Retrieves a list of all city objects of a state id'''
    state = storage.get(State, state_id)
    if state is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    list_cities = [city.to_dict() for city in state.cities]
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a city object by ID"""
    city = storage.get(City, city_id)
    if city is not None:
        return jsonify(city.to_dict())
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object by ID"""
    city = storage.get(City, city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a new city"""
    state = storage.get(State, state_id)
    if state is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request_data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_city = City(name=request_data['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a State object by ID"""
    city = storage.get(City, city_id)
    if city is None:
        return make_response(jsonify({'error': 'not found'}), 404)
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
