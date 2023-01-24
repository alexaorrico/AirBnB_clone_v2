#!/usr/bin/python3
"""ALX SE Flask Api City Module."""
from api.v1.app import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id: str):
    """Return list of all cities link to the current state."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id: str):
    """Return a city given its id."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id: str):
    """Delete a city given its id from storage."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route(
        '/states/<state_id>/cities',
        methods=['POST'],
        strict_slashes=False)
def create_city(state_id: str):
    """Create a new city in storage."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        city_attrs = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if 'name' not in city_attrs:
        abort(400, 'Missing name')
    city = City(**city_attrs)
    city.state_id = state_id
    storage.new(city)
    storage.save()

    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id: str):
    """Update a city given its id."""
    try:
        city_attrs = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for attr, value in city_attrs.items():
        if attr not in ('id', 'state_id', 'updated_at', 'created_at'):
            setattr(city, attr, value)
    city.save()
    return jsonify(city.to_dict())
