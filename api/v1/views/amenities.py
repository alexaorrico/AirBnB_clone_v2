#!/usr/bin/python3
"""objects that handles all default RestFul API actions for cities"""

from flask import abort, request, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<string:state_id>/cities", strict_slashes=False)
def get_cities(state_id):
    """Method for list all cities from state"""
    new_list = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities:
        new_list.append(city.to_dict())
    return jsonify(new_list)


@app_views.route("/cities/<string:city_id>", strict_slashes=False)
def one_city(city_id):
    """Method for list one city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<string:city_id>", methods=["DELETE"],
                 strict_slashes=False)
def city_delete(city_id):
    """Method that deletes a city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify(({})), 200)


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_post(state_id):
    """Method that creates a city"""
    state = storage.get(State, state_id)
    data = request.get_json()
    if not state:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")
    if "name" not in data:
        abort(400, description="Missing name")
    data['state_id'] = state_id
    instance = State(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/cities/<string:city_id>", methods=['PUT'],
                 strict_slashes=False)
def city_put(city_id):
    """Method that puts a city"""
    city = storage.get(City, city_id)
    data = request.get_json()
    if not city:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at', 'state_id']

    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
