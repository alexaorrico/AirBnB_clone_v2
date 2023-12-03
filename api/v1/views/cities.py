#!/usr/bin/python3

"""
Module for handling HTTP requests related to City objects
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<string:state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state_id(state_id):
    """
    Retrieve all cities with the given state id
    """
    state_instance = storage.get(State, state_id)
    if state_instance is None:
        abort(404, "State not found")
    cities_list = [city.to_dict() for city in state_instance.cities]
    return jsonify(cities_list)


@app_views.route("/cities/<string:city_id>", methods=['GET'],
                 strict_slashes=False)
def get_city_by_id(city_id):
    """
    Retrieve a city with the given id
    """
    city_instance = storage.get(City, city_id)
    if city_instance is None:
        abort(404, "City not found")
    return jsonify(city_instance.to_dict())


@app_views.route("/cities/<string:city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """
    Delete a city with the given id
    """
    city_instance = storage.get(City, city_id)
    if city_instance is None:
        abort(404, "City not found")
    storage.delete(city_instance)
    return jsonify({}), 200


@app_views.route("/states/<string:state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city_with_state_id(state_id):
    """
    Create a city with the given state id
    """
    state_instance = storage.get(State, state_id)
    if state_instance is None:
        abort(404, "State not found")
    res = request.get_json()
    if res is None:
        abort(400, 'Not a JSON')
    if 'name' not in res:
        abort(400, 'Missing "name"')
    new_city_instance = City(**res)
    new_city_instance.state_id = state_id
    new_city_instance.save()
    return jsonify(new_city_instance.to_dict()), 201


@app_views.route("/cities/<string:city_id>", methods=['PUT'],
                 strict_slashes=False)
def update_city_by_id(city_id):
    """
    Update a city with the given id
    """
    city_instance = storage.get(City, city_id)
    if city_instance is None:
        abort(404, "City not found")
    res = request.get_json()
    if res is None:
        abort(400, 'Not a JSON')
    for k, v in res.items():
        setattr(city_instance, k, v)
    city_instance.save()
    return jsonify(city_instance.to_dict()), 200
