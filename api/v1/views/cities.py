#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import abort, request, jsonify


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["GET"])
def new_cities(state_id):
    """showing cities"""
    city_list = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    newCities = state.cities
    for city in newCties:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["POST"])
def create_new_city(state_id):
    """creating a new city"""
    newState = storage.get(State, state_id)
    if newState is None:
        abort(404)
    request_json = request.get_json(force=True, silent=True)
    if not request_json:
        abort(400, "Not a JSON")
    if "name" not in request_json:
        abort(400, "Missing name")
    new_state = City(state_id=state.id, **request_json)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def delete_city(city_id):
    """deleting a city"""
    new_obj = storage.get(City, city_id)
    if new_obj is None:
        abort(404)
    storage.delete(new_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def cities_id(city_id):
    """getting a City"""
    new_city = storage.get(City, city_id)
    if new_city is None:
        abort(404)
    return jsonify(new_city.to_dict())


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def update_city(city_id):
    """updating city"""
    new_obj = storage.get(City, city_id)
    if new_obj is None:
        abort(404)
    request_json = request.get_json(force=True, silent=True)
    if not request_json:
        abort(400, "Not a JSON")
    new_obj.name = request_json.get("name", new_obj.name)
    new_obj.save()
    return jsonify(new_obj.to_dict()), 200
