#!/usr/bin/python3
"""The `cities` module"""


from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=True)
def list_all_cities():
    """Lists all cities in a particular state with state_id"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify([cities.to_dict() for cities in state.cities])


@app_views.route("/cities/<city_id>",
                 methods=["GET"], strict_slashes=True)
def list_city_id(state_id):
    """Retrives a city by id"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>",
                 methods=["DELETE"], strict_slashes=True)
def delete_city(city_id):
    """Deletes a city by id"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=True)
def create_city():
    """Creates a new city"""
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    if "name" not in payload:
        abort(400, "Missing name")
    new_city = City(**payload)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>",
                 methods=["PUT"], strict_slashes=True)
def update_city_id(city_id):
    """Updates city by id"""
    city = storage.get("City", city_id):
        if not city:
            abort(404)
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    for key, value in payload.items():
        if key not in {"id", "state_id", "created_at", "updated_at"}:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
