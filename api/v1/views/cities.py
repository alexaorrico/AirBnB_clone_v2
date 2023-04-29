#!/usr/bin/python3
"""Creates a view for City objects"""

import json
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import abort, request, jsonify


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """gets all the cities associated with the state_id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in storage.all(City).values()
              if city.state_id == state_id]
    return jsonify(cities), 200


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """gets a single city based on it's id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes a city from db"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """adds a new city to the db"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    obj = request.get_json()
    if 'name' not in obj:
        abort(400, "Missing name")
    obj['state_id'] = state_id
    city = City(**obj)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
