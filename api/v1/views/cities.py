"""Module providing API endpoints for City resources."""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieve a list of cities for a specific state."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities_list = [city.to_dict() for city in state.cities]
    return jsonify(cities_list)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieve information about a specific city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a city by its ID."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create a new city for a specific state."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
        if 'name' not in data:
            return jsonify({"error": "Missing name"}), 400

        city = City(**data)
        city.state_id = state_id
        storage.new(city)
        storage.save()

        return jsonify(city.to_dict()), 201
    else:
        return jsonify({"error": "Not a JSON"}), 400

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Update a city's information."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
        keys_to_ignore = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in keys_to_ignore:
                setattr(city, key, value)
        city.save()

        return jsonify(city.to_dict()), 200
    else:
        return jsonify({"error": "Not a JSON"}), 400
