#!/usr/bin/python3
"""
State view module
"""
from models import storage
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_state_cities(state_id):
    """Gets all cities of a state."""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def post_state_cities(state_id):
    """Creates a cities with a state id."""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        return "Not a JSON", 400
    if "name" not in json_data:
        return "Missing name", 400
    json_data["state_id"] = state_id
    new_city = City(**json_data)
    new_city.save()
    return new_city.to_dict(), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city_by_id(city_id):
    """Gets a city by id."""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return city.to_dict()


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city_by_id(city_id):
    """Deletes a city by id."""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    return {}, 200


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def put_city_by_id(city_id):
    """Updates a city by id."""
    ignore = ["id", "state_id", "created_at", "updated_at"]
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        return "Not a JSON", 400
    for key in json_data:
        if key not in ignore:
            setattr(city, key, json_data[key])
    city.save()
    return city.to_dict(), 200
