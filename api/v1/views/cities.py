#!/usr/bin/python3
"""handles all defaults RESTful API actions for cities"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """retrieves all cities of a given state"""
    state = storage.get(State, state_id)
    if state:
        cities = storage.all(City)
        city_list = []

        for city in cities.values():
            if city.state_id == state_id:
                city_list.append(city.to_dict())
        return jsonify(city_list)
    abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_city_id(city_id):
    """retrieves a city based on a given id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes a city based on its id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """creates a new city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    if "name" not in data:
        return abort(400, "Missing name")
    city = City()
    city.state_id = state_id
    city.name = data["name"]
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """updates a given city"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
