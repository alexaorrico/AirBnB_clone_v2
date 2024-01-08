#!/usr/bin/python3
"""
Module for state api
"""
from flask import Flask, jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def get_cities_objs(state_id):
    """returning all cities related to state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    my_cities = [city.to_dict() for city in state.cities]
    return jsonify(my_cities)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """getting a city of specific id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """ deletes a city object based on given id """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return (jsonify({})), 200


@app_views.route('states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def post_city(state_id):
    """ adds new city based on given state id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    if 'name' not in json_data:
        return jsonify({"error": "Missing name"}), 400
    json_data['state_id'] = state_id
    city = City(**jsonx_data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def updating_city(city_id):
    """ updates a city based on given id """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    for key, val in json_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200
