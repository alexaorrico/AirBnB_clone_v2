#!/usr/bin/python3
"""Modules that handles all Restful API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_cities(state_id):
    """Retrieves the list of all cities"""
    all_states = storage.get(State, state_id)
    if all_states is None:
        abort(404)
    cities_list = []
    for city in all_states.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city(city_id):
    """Retrieves a city"""
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    return jsonify(cities.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """Creates a new city"""
    id_state = storage.get('State', state_id)
    if id_state is None:
        abort(404)
    new_city = request.get_json()
    if new_city is None:
        abort(404)
    if not new_city:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in new_city:
        return jsonify({'error': 'Missing name'}), 400
    else:
        new_city['state_id'] = state_id
        new_obj = City(**new_city)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a given city"""
    city_to_update = request.get_json()
    if city_to_update is None:
        abort(404)
    if not city_to_update:
        return jsonify({'error': 'Not a JSON'}), 400

    city_dict = storage.get(City, city_id)
    ignore_list = ['id', 'created_at', 'updated_at']
    if city_dict:
        for key, value in city_to_update.items():
            setattr(city_dict, key, value)
        storage.save()
        return jsonify(city_dict.to_dict()), 200
    else:
        abort(404)
