#!/usr/bin/python3
"""States"""


from flask import jsonify, Response, abort, request, make_response
from werkzeug.exceptions import BadRequest
import json
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieves the list of all City
    objects associated with a given state."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_by_id(city_id):
    """Retrieve a city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """
    Creates a new city
    """
    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json()
    if 'name' not in data:
        return make_response("Missing name", 400)

    new_city = City(name=data["name"], state_id=state_id)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update an existing city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        raise BadRequest('Not a JSON', 400)
    data = request.get_json(silent=True)
    for key, value in data.items():
        # Ignore keys: id, created_at, state_id,  and updated_at
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
