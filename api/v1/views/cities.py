#!/usr/bin/python3
"""
Handles RESTFul API actions for amenities
"""

from flask import abort
from api.v1.views import app_views
from flask import jsonify
from flask import request
from models.city import City
from models import storage


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def all_cities(state_id):
    """
    Returns list of all cities in a state
    """
    state = storage.get("State", state_id)
    if state:
        cities = state.cities
        list_cities = []
        for city in cities:
            list_cities.append(city.to_dict())
        return jsonify(list_cities)
    abort(404)

@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def one_city(city_id):
    """
    Returns a city object based on id
    """
    city = storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Returns a city object based on id
    """
    city = storage.get("City", city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/states/<state_id>/cities", methods=['POST'], strict_slashes=False)
def add_city(state_id):
    """
    Adds a city of a state based on data provided
    """
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, "Missing name")

    city_name = data['name']
    state = storage.get("State", state_id)
    if state:
        new_city = City(name=city_name, state_id=state_id)
        new_city.save()
        return jsonify(new_city.to_dict()), 201
    abort(404)

@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates a city object based on data provided
    """
    city = storage.get("City", city_id)
    if city:
        data = request.get_json(silent=True)
        if not data:
            abort(400, "Not a JSON")
        keys_to_ignore = ["created_at", "id", "updated_at"]
        for k, v in data.items():
            if k not in keys_to_ignore:
                setattr(city, k, v)
        storage.save()
        return jsonify(city.to_dict()), 200
    abort(404)
