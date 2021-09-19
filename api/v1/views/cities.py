#!/usr/bin/python3
"""Cities view for api v1"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_all_cities_from_state(state_id):
    """
        All city objects related to a state object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    return jsonify([city.to_dict() for city in cities]), 200


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city_by_id(city_id):
    """
        A city object based on its id. Error if not found
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """
        Stores and returns a new city in a given state
    """
    city_json = request.get_json(silent=True)
    if not city_json:
        return jsonify({'error': 'Not a JSON'}), 400
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if 'name' not in city_json:
        return jsonify({'error': 'Missing name'}), 400
    city_json['state_id'] = state_id
    city = City(**city_json)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """
        Updates and returns the information of a given city
    """
    city_json = request.get_json(silent=True)
    if not city_json:
        return jsonify({'error': 'Not a JSON'}), 400
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for key, val in city_json.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """
        Deletes a city with id and returns an empty JSON
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200
