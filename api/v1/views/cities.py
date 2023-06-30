#!/usr/bin/python3
"""Create a new view for City objects that handles all
default RESTFul API actions."""

from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Get all cities of a given state."""
    state = storage.get(State, state_id)
    if not state:
        return jsonify([])
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/api/v1/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Get details of a specific city."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/api/v1/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete a specific city."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route('/api/v1/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Create a new city in a specific state."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    city_data = request.get_json()
    if 'name' not in city_data:
        abort(400, description="Missing name")

    new_city = City(**city_data)
    new_city.state_id = state_id
    new_city.save()

    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/api/v1/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Update an existing city."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    city_data = request.get_json()
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in city_data.items():
        if key not in ignore:
            setattr(city, key, value)

    storage.save()

    return jsonify(city.to_dict())
