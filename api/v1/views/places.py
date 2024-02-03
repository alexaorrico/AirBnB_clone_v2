#!/usr/bin/python3
"""This module contains the view for the place resource.

city_places: handler for city's places
places: handler for places
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route(
    "/cities/<city_id>/places",
    methods=["GET", "POST"],
    strict_slashes=False,
)
def city_places(city_id):
    """Handler for places in existing cities."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        return jsonify([place.to_dict() for place in city.places])
    elif request.method == "POST":
        if not request.is_json:
            return jsonify({"error": "Not a JSON"}), 400
        body = request.get_json(force=True)
        user_id = body.get("user_id", None)
        if user_id is None:
            return jsonify({"error": "Missing user_id"}), 400
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        if body.get("name", None) is None:
            return jsonify({"error": "Missing name"}), 400
        body.update({"city_id": city_id})
        new_place = Place(**body)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201
    abort(405)


@app_views.route(
    "/places/<place_id>", methods=["GET", "PUT", "DELETE"],
    strict_slashes=False)
def places(place_id):
    """Handler for places."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict())
    elif request.method == "PUT":
        if not request.is_json:
            return jsonify({"error": "Not a JSON"}), 400
        body = request.get_json(force=True)
        for name, value in {
            k: v
            for k, v in body.items()
            if k
            not in [
                "id", "created_at",
                "updated_at", "user_id", "city_id",
            ]
        }.items():
            setattr(place, name, value)
        place.save()
        return jsonify(place.to_dict()), 200
    elif request.method == "DELETE":
        place.delete()
        storage.save()
        return jsonify({}), 200
    abort(405)
