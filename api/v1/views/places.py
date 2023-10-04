#!/usr/bin/python3
"""The `place` module"""


from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=True)
def list_all_cities():
    """Lists all places of a particular city with city_id"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify([places.to_dict() for places in city.places])


@app_views.route("/places/<place_id>",
                 methods=["GET"], strict_slashes=True)
def list_place_id(place_id):
    """Retrives a place from a city by city_id"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=True)
def delete_place(place_id):
    """Deletes a place by id"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=True)
def create_place():
    """Creates a new place by city_id"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    if "user_id" not in payload:
        abort(400, "Missing user_id")
    user = storage.get("User", payload["user_id"])
    if not user:
        abort(404)
    if "name" not in payload:
        abort(404, "Missing name")
    new_place = Place(**payload)
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>",
                 methods=["PUT"], strict_slashes=True)
def update_place_id(place_id):
    """Updates place by id"""
    place = storage.get("Place", place_id):
        if not place:
            abort(404)
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    for key, value in payload.items():
        if key not in {"id", "user_id", "city_id", "created_at", "updated_at"}:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
