#!/usr/bin/python3
"""
Contains the cities view for the AirBnB clone v3 API.
Handles all default RESTful API actions for City objects.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all City objects of a State.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a City in a State.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, description='Not a JSON')
    if 'name' not in request_data:
        abort(400, description='Missing name')
    request_data['state_id'] = state_id
    city = City(**request_data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates a City object.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, description='Not a JSON')
    for key, value in request_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
