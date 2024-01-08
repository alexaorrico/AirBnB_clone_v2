#!/usr/bin/python3
"""
a new view for City objects that handles all default RESTFul API actions.
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities_by_state(state_id):
    """
    Retrieves the list of all City obj of a State or creates a new City.

    GET /api/v1/states/<state_id>/cities - Retrieves cities of a state
    POST /api/v1/states/<state_id>/cities - Creates a new State

    Args:
    state_id (str): ID of the State.

    Returns:
    JSON: List of City obj or newly created City.
    """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if request.method == 'GET':
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)

    if request.method == 'POST':
        try:
            data = request.get_json()
        except Exception:
            abort(400, 'Not a JSON')

        if data is None:
            abort(400, 'Not a JSON')

        if 'name' not in data:
            abort(400, 'Missing name')

        city = City(**data)
        city.state_id = state_id
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def city_by_id(city_id):
    """
    Retrieves, updates, or deletes a City object by ID.

    GET /api/v1/cities/<city_id> - Retrieves a City object.
    PUT /api/v1/cities/<city_id> - Updates a City object.
    DELETE /api/v1/cities/<city_id> - Deletes a City object.

    Args:
    city_id (str): ID of the City.

    Returns:
    JSON: City obj or success message.
    """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'PUT':
        try:
            data = request.get_json()
        except Exception:
            abort(400, 'Not a JSON')

        if data is None:
            abort(400, 'Not a JSON')

        if 'name' not in data:
            abort(400, 'Missing name')

        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({}), 200
