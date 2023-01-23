#!/usr/bin/python3
''' Serve Cities '''

from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def get_city(state_id=None):
    """
    Returns list of City objects linked to any State
    with state_id: Returns a single state object
    without state_id: 404
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['GET'])
def get_city_id(city_id):
    '''
    Get city by city id
    '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """
    Deletes a city from the database
    """
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    cities.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("states/<state_id>/cities", strict_slashes=False,
                 methods=['POST'])
def post_city(state_id=None):
    """
    Post a city
    """
    state_key = "State." + str(state_id)
    if state_key not in storage.all(State).keys():
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    city = City(**request.get_json())
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def update_city(city_id=None):
    """ Update a state object
    """
    key = "City." + str(city_id)
    if key not in storage.all(City).keys():
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
