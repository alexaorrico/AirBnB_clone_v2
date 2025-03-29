#!/usr/bin/python3
""" Cities """

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cities(state_id):
    """retrieve all cities"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """get city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """create a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    payload = request.get_json()
    payload["state_id"] = state_id
    city = City(**payload)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Update a State object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    payload = request.get_json()
    ignore_keys = ["id", "state_id", "created_at", "updated_at"]
    for key, value in payload.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), '200'


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), '200'
