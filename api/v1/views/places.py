#!/usr/bin/python3
"""restful API functions for City"""
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from flask import request, jsonify, abort


@app_views.route(
        "/cities/<city_id>/places", strict_slashes=False,
        methods=["GET", "POST"])
def cities_end_points(city_id):
    """city objects that handles all default RESTFul API actions"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == "GET":
        places = [place.to_dict() for place in city.places]
        return jsonify(places), 200

    elif request.method == "POST":
        data = request.get_json()
        if not data or not isinstance(data, dict):
            abort(400, "Not a JSON")
        if not data.get("name"):
            abort(400, "Missing name")
        if not data.get("user_id"):
            abort(400, "Missing user_id")
        user = storage.get(User, data["user_id"])
        if not user:
            abort(404)
        data["city_id"] = city_id
        new_place = Place(**data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route(
        "/places/<place_id>", strict_slashes=False,
        methods=["DELETE", "PUT", "GET"])
def place_end_points(place_id):
    """city objects that handles all default RESTFul API actions"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == "GET":
        return jsonify(place.to_dict()), 200

    elif request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        data = request.get_json()
        if not data or not isinstance(data, dict):
            abort(400, "Not a JSON")
        ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
