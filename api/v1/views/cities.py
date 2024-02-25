#!/usr/bin/python3
"""Cities hanlders."""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.city import City


@app_views.route(
    "/states/<string:state_id>/cities", methods=["GET"], strict_slashes=False
)
def get_cities(state_id):
    """Retrieve all the cities of the specified state."""
    state = storage.get("State", state_id)
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
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
    "/cities/<string:city_id>", methods=["DELETE"], strict_slashes=False
)
def delete_city(city_id):
    """Delete specified city."""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route(
    "/states/<string:state_id>/cities", methods=["POST"], strict_slashes=False
)
def create_city(state_id):
    """Create a new city."""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    kwargs = request.get_json()
    kwargs["state_id"] = state_id
    city = City(**kwargs)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route(
    "/cities/<string:city_id>", methods=["PUT"], strict_slashes=False
)
def update_city(city_id):
    """Update specified city."""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for attr, val in request.get_json().items():
        if attr not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, attr, val)
    city.save()
    return jsonify(city.to_dict())
