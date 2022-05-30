#!/usr/bin/python3
"""
State objects that handles all default RestFul API actions
"""

from models.base_model import BaseModel
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all City objects
    """
    state = storage.get('State', state_id)
    cities_list = []
    if state:
        for city in state.cities:
            cities_list.append(city.to_dict())
        return jsonify(cities_list)
    else:
        abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object
    """
    city = storage.get('City', city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Delete a City object
    """
    city = storage.get('City', city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities",
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """
    Create a City object
    """
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    _data = request.get_json()
    state = storage.get('State', state_id)
    if state:
        city = City(**_data)
        city.state_id = state_id
        storage.save()
        _response = jsonify(city.to_dict())
        _response.status_code = 201
        return _response
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Update a State object
    """
    if not request.is_json:
        abort(400, "Not a JSON")
    city = storage.get('City', city_id)
    if city:
        _data = request.get_json()
        to_avoid = ['id', 'created_at', 'updated_at']
        for name, value in _data.items():
            if name not in to_avoid:
                setattr(city, name, value)
        storage.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)
