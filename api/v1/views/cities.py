#!/usr/bin/python3
"""
Cities API view for handling RESTful actions
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route(
        '/states/<state_id>/cities',
        methods=['GET'],
        strict_slashes=False
        )
def get_cities(state_id):
    """
    Retrieve all cities of a given state
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieve a single city identified by ID
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
        '/states/<state_id>/cities',
        methods=['POST'],
        strict_slashes=False
        )
def create_city(state_id):
    """
    Create a new City in a given State
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    if 'name' not in request.json:
        abort(400, description="Missing name")

    new_city = City(name=request.json['name'], state_id=state_id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Update a City object idenfified by valid city id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    for key, value in request.json.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Delete a City object identified by city id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200
