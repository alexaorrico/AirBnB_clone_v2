#!/usr/bin/python3
"""
cities.py
"""
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State
import json

from . import app_views

@app_views.route('states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def cities_per_id(state_id):
    """
    Retrieves the list of all City
    objects of a State
    """
    desired_cities = []
    for key, value in storage.all(City).items():
        if value.state_id == state_id:
            desired_cities.append(value.to_dict())
    if desired_cities:
        return jsonify(desired_cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_by_id(city_id):
    """
    retrieves one city per id
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    deletes city
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def POST_city(state_id):
    """
    add city
    """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_city = City()
    setattr(new_city, "state_id", state_id)
    setattr(new_city, "name", data["name"])
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """
    updates city
    """
    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json()
    check = ["id", "created_at", "updated_at", "state_id"]
    city = storage.get(City, city_id)
    if city:
        for key, value in data.items():
            if key not in check:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)
