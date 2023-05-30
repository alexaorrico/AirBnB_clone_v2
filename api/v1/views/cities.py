#!/usr/bin/python3
"""RESTful API functions for City"""
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage
from flask import request, jsonify, abort


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False,
                 methods=["GET", "POST"])
def cities_end_points(state_id):
    """Handles all default RESTful API actions for city objects"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == "GET":
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)

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


@app_views.route("/cities/<city_id>",
                 strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def city_end_points(city_id):
    """Handles all default RESTful API actions for a city object"""
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
