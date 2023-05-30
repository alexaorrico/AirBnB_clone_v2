#!/usr/bin/python3
""" RESTFul API for cities"""
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views

def get_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return state


@app_views.route("/states/<state_id>/cities", strict_slashes=False, methods=["GET", "POST"])
def states_end_points(state_id):
    state = get_state(state_id)
    obj_cities = storage.all(City)
    cities_dict = [obj.to_dict() for obj in obj_cities.values() if obj.state_id == state_id]

    if request.method == "GET":
        return jsonify(cities_dict)

    elif request.method == "POST":
        data = request.get_json()
        if not data or not isinstance(data, dict):
            abort(400, "Not a JSON")
        if "name" not in data:
            abort(400, "Missing name")

        data["state_id"] = state_id
        new_city = City(**data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE", "PUT", "GET"])
def city_end_points(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == "GET":
        return jsonify(city.to_dict())

    elif request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        data = request.get_json()
        if not data or not isinstance(data, dict):
            abort(400, "Not a JSON")

        ignore_keys = ["id", "state_id", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
