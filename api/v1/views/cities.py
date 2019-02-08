#!/usr/bin/python3
"""Module to create a new view for City objects"""
from flask import jsonify, Flask, request, abort
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state_id(state_id):
    """Retrieves the list of all City objects of a State by state_id"""
    state = storage.get('State', state_id)
    list_of_cities = []
    if state is None:
        abort(404)
    for element in state.cities:
        list_of_cities.append(element.to_dict())
    return jsonify(list_of_cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city_id(city_id):
    """Retrieves the list of all City objects of a State by state_id"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """Deletes a state by ID"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Post a City object"""

    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    data['state_id'] = state_id
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Put a City object"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for k, v in data.items():
        if k not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, k, v)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 200
