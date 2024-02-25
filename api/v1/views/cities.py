#!/usr/bin/python3
"""Cities hanlders."""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route(
    "/states/<string:state_id>/cities", methods=["GET"], strict_slashes=False
)
def get_cities(state_id):
    """Retrieve all the cities of the specified state."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route(
    "/cities/<string:city_id>",
    methods=["GET"],
    strict_slashes=False,
)
def get_city(city_id):
    """Get info about specified city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
    "/cities/<string:city_id>", methods=["DELETE"], strict_slashes=False
)
def delete_city(city_id):
    """Delete specified city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route(
    "/states/<string:state_id>/cities", methods=["POST"], strict_slashes=False
)
def create_city(state_id):
    """Create a new city."""
    req = request.get_json(silent=True)
    if not req:
        abort(400, "Not a JSON")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if "name" not in request.get_json():
        abort(400, "Missing name")
    req["state_id"] = state_id
    city = City(**req)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route(
    "/cities/<string:city_id>", methods=["PUT"], strict_slashes=False
)
def update_city(city_id):
    """Update specified city."""
    req = request.get_json(silent=True)
    if not req:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for attr, val in request.get_json().items():
        if attr not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, attr, val)
    city.save()
    return jsonify(city.to_dict())
