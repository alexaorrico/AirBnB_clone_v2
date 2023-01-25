#!/usr/bin/python3
"""Place view"""

from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_place_in_city(city_id=None):
    """
    Retrives all places of a given city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(place)


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def get_place(place_id=None):
    """
    retrieve a single place with the id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """
    delete a single place when passed the id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id=None):
    """
    create a new place in a city
    """
    key = "City." + str(city_id)
    if key not in storage.all(City).keys():
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")
    if storage.get(User, request.get_json()["user_id"]) is None:
        abort(404)
    if "name" not in request.get_json():
        abort(400, "Missing name")
    place = Place(**request.get_json())
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id=None):
    """
    update the user which the id is passed
    """
    key = "Place." + str(place_id)
    if key not in storage.all(Place).keys():
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    place = storage.get(Place, place_id)
    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
