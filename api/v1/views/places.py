#!/usr/bin/python3
"""
Handles RESTFul API actions for amenities
"""

from flask import abort
from api.v1.views import app_views
from flask import jsonify
from models.place import Place
from flask import request
from models import storage


@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def places_in_city(city_id):
    """
    Returns list of places in a city
    """
    city = storage.get("City", city_id)
    if city:
        all_places = storage.all("Places")
        city_places = []
        for place in all_places.values():
            if place.city_id == city_id:
                city_places.append(place.to_dict())
        return jsonify(city_places)
    abort(404)


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def one_place(place_id):
    """
    Returns a place object based on id
    """
    place = storage.get("Place", place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a place object based on id
    """
    place = storage.get("Place", place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'], strict_slashes=False)
def add_place(city_id):
    """
    Adds a place object based on data provided
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get("User", data["user_id"])
    if user is None:
        abort(404)
    if "name" not in data:
        abort(400, "Missing name")
    data.update()
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    Updates a place object based on data provided
    """
    place = storage.get("Place", place_id)
    if place:
        data = request.get_json(silent=True)
        if not data:
            abort(400, "Not a JSON")
        keys_to_ignore = ["created_at", "id", "updated_at", "city_id", "user_id"]
        for k, v in data.items():
            if k not in keys_to_ignore:
                amenity.__dict__.update({k: v})
        storage.save()
        return jsonify(amenity.to_dict()), 200
    abort(404)
