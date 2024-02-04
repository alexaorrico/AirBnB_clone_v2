#!/usr/bin/python3
"""
module for CRUD city object
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities_of_state(state_id):
    """ get all cities of belongs to state_id"""
    state = storage.get(State, state_id)
    json_obj = [c.to_dict() for c in state.cities]
    if not state:
        abort(404)
    return jsonify(json_obj)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """ return city by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """ remove city from storage"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """ create new city into storage"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if 'name' not in data:
        abort(400, "Missing name")
    new_data = data.copy()
    new_data["state_id"] = state_id
    new_city = City(**new_data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ update existing city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
