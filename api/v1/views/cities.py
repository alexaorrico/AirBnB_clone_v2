#!/usr/bin/python3
"""
cities view routes
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route(
    "/states/<state_id>/cities",
    methods=["GET", "POST"],
    strict_slashes=False,
)
def state_cities(state_id):
    """Handles /states/<state_id>/cities endpoint

    Returns:
        json: list of all cities or the newly added city
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == "POST":
        city_data = request.get_json(silent=True)
        if city_data is None:
            return jsonify(error="Not a JSON"), 400

        if "name" not in city_data:
            return jsonify(error="Missing name"), 400
        else:
            city_data["state_id"] = state.id
            city = City(**city_data)
            storage.new(city)
            storage.save()
            return jsonify(city.to_dict()), 201

    else:
        return jsonify([city.to_dict() for city in state.cities])


@app_views.route(
    "/cities/<city_id>",
    methods=["GET", "DELETE", "PUT"],
    strict_slashes=False,
)
def cities(city_id):
    """Handles /cities endpoint

    Returns:
        json: list of all cities or the newly added city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return jsonify({})
    elif request.method == "PUT":
        city_data = request.get_json(silent=True)
        if city_data is None:
            return jsonify(error="Not a JSON"), 400

        for key, value in city_data.items():
            if key not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict())

    else:
        return jsonify(city.to_dict())
