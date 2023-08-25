#!/usr/bin/python3
"""imports"""
from models.city import City
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_city_by_state(state_id):
    """Return cities in state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_list = []
    for city in state.cities:
        city_list.append(city.to_dict())
    return jsonify(city_list), 200


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_id(city_id):
    """Return city with id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Dele city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return ({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    data['state_id'] = state.id
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Returns the City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    ignored_keys = {'id', 'created_at', 'updated_at'}
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200