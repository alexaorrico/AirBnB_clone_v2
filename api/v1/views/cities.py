#!/usr/bin/python3
"""This is the views for the cities model"""

from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities_by_state_id(state_id):
    """Get all the cities in a state identified by state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_cities = [city.to_dict() for city in state.cities]
    return jsonify(state_cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city_by_id(city_id):
    """Get a city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delelte_city_by_id(city_id):
    """Deletes a city object by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a city with the specified state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json().keys():
        return make_response(jsonify({"error": "Missing name"}), 400)
    city = City(**request.get_json())
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city_by_id(city_id):
    """Updates a city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict())
