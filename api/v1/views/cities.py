#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import abort, request, jsonify


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["GET"])
def cities(state_id):
    """show cities"""
    cities_list = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def cities_id(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def city_delete(city_id):
    """delete method"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["POST"])
def create_city(state_id):
    """create a new post req"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = City(state_id=state.id, **data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def update_city(city_id):
    """update city"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    obj.name = data.get("name", obj.name)
    obj.save()
    return jsonify(obj.to_dict()), 200