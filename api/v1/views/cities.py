#!/usr/bin/python3
"""
Contains the Citys API routes
"""

from flask import Flask, jsonify, abort, request
from models import storage
from models.state import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    city = City(**data)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
