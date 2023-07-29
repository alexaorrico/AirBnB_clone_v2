#!/usr/bin/python3
"""city obj API"""
from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_in_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities_list = [city.to_dict() for city in state.cities]
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id=None):
    """Get all cities or a cities whose id is specified"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Create a new city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city = request.get_json()
    if not city:
        abort(400, description="Not a JSON")
    if 'name' not in city:
        abort(400, description="Missing name")
    city['state_id'] = state_id
    obj = City(**city)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Update a city object"""
    city = storage.get(City, city_id)
    fixed_data = ['id', 'created_at', 'updated_at']
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in fixed_data:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
