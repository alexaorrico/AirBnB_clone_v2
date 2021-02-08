#!/usr/bin/python3
"""Cities objects that handles all default RestFul API actions
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_of_state(state_id):
    """Retrieve a list of Cities objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_cities = [cities.to_dict() for cities in state.cities]
    return jsonify(state_cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def obj_city(city_id):
    """Retrieve a specific city object """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_cities(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a City object"""
    if request.get_json() is None:
        return "Not a JSON", 400
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    elif 'name' not in request.get_json():
        return "Missing name", 400
    else:
        city = City(**request.get_json())
        city.state_id = state_id
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def Update_city(city_id):
    """Update a city store in the storage"""
    if request.get_json() is None:
        return "Not a JSON", 400
    city = storage.get(City, city_id)
    if city:
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in request.get_json().items():
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)
