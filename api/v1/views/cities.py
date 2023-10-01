# api/v1/views/cities.py

from flask import Flask, jsonify, request, abort
from models import storage, State
from models.city import City
from api.v1.views import app_views

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieve the list of all City objects of a State."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieve a City object by ID."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a City object by ID."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create a new City."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_city = City(**data)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a City object by ID."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    # Remove keys that should be ignored
    data.pop("id", None)
    data.pop("state_id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    for key, value in data.items():
        setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
