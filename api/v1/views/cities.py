#!/usr/bin/python3

"""
Module for handling HTTP requests for City objs
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<string:state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_cities_stateid(state_id):
    """
    Retrieves cities using state id
    """
    state_instance = storage.get(State, state_id)
    if state_instance is None:
        abort(404, "State not found")
    cities_list = [city.to_dict() for city in state_instance.cities]
    return jsonify(cities_list)


@app_views.route("/cities/<string:city_id>", methods=['GET'],
                 strict_slashes=False)
def get_city_id(city_id):
    """
    Retrieves a city of a specified id
    """
    city_instance = storage.get(City, city_id)
    if city_instance is None:
        abort(404, "City not found")
    return jsonify(city_instance.to_dict())


@app_views.route("/cities/<string:city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city_id(city_id):
    """
    Deletes a city of specified id
    """
    city_instance = storage.get(City, city_id)
    if city_instance is None:
        abort(404, "City not found")
    storage.delete(city_instance)
    return jsonify({}), 200


@app_views.route("/states/<string:state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city_state_id(state_id):
    """
    Creates a city using state id
    """
    state_instance = storage.get(State, state_id)
    if state_instance is None:
        abort(404, "State not found")
    result = request.get_json()
    if result is None:
        abort(400, 'Not a JSON')
    if 'name' not in result:
        abort(400, 'Missing "name"')
    new_city_instance = City(**result)
    new_city_instance.state_id = state_id
    new_city_instance.save()
    return jsonify(new_city_instance.to_dict()), 201


@app_views.route("/cities/<string:city_id>", methods=['PUT'],
                 strict_slashes=False)
def update_city_id(city_id):
    """
    Updates a city with a specified id
    """
    city_instance = storage.get(City, city_id)
    if city_instance is None:
        abort(404, "City not found")
    result = request.get_json()
    if result is None:
        abort(400, 'Not a JSON')
    for i, v in result.items():
        setattr(city_instance, i, v)
    city_instance.save()
    return jsonify(city_instance.to_dict()), 200
