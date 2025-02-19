#!/usr/bin/python3
"""
Create a new view for Place objects
that handles all default RESTFul API actions
"""
from flask import Flask, jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
import json


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    cities_list = [place.to_dict() for place in city.places]
    response = make_response(json.dumps(cities_list, indent=2) + "\n")
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data["user_id"])

    if not user:
        abort(404)

    if "name" not in request.get_json():
        abort(400, description="Missing name")

    new_place = Place(city_id=city_id, **data)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def updata_place(place_id):
    """Updates a User object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    for k, v in data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(place, k, v)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
