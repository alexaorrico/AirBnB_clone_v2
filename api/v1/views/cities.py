#!/usr/bin/python3
"""
new view for City objects that
handles all default RESTFul API actions
"""

import json
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all City objects
    for a specified State
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route(
    '/cities/<city_id>',
    methods=['GET'],
    strict_slashes=False
    )
def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route(
    '/cities/<city_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def del_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()
    return {}, 200


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False)
def create_city_by_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
        return
    try:
        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if data.get('name') is None:
            return make_response(jsonify({'error': 'Missing name'}), 400)
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    data.update({'state_id': state_id})
    obj = City(**data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route(
    '/cities/<city_id>',
    methods=['PUT'],
    strict_slashes=False)
def update_city(city_id):
    """update operation"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)

    try:
        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if data.get('name') is None:
            return make_response(jsonify({'error': 'Missing name'}), 400)
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for k, v in data.items():
        if k not in ['state_id', 'id', 'created_at', 'updated_at']:
            setattr(obj, k, v)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
