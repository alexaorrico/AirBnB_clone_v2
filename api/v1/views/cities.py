#!/usr/bin/python3
"""
cities.py
"""
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State
from . import app_views


@app_views.route('states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """
    Retrieves the list of all City
    objects of a State
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """
    retrieves one city per id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    deletes city
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """
    add city
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
    """
    updates city
    """
    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json()
    check = ["id", "created_at", "updated_at", "state_id"]
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for key, value in data.items():
        if key not in check:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
