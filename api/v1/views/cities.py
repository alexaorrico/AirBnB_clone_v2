#!/usr/bin/python3
"""
This Module contains City objects
that handles all default RESTFul API actions
"""
from flask import Flask, abort, make_response, request, jsonify
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """retriveves all cities linked to a state"""
    cities_list = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=True)
def get_city(city_id):
    """retrieve a particular city based on its ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a particular city based on its ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_cities(state_id):
    """creates a city object of a state"""
    required_key = 'name'
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    json_request = request.get_json()
    if not json_request:
        abort(400, "Not a JSON")
    if required_key not in json_request:
        abort(400, "Missing Name")

    city = City(state_id=state_id, **json_request)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=True)
def put_city(city_id):
    """updates a particular city based on its ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_request = request.get_json()
    if not json_request:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in json_request.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
