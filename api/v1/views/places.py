#!/usr/bin/python3
"""Create a new view for Place object that
handles all default RESTFul API actions"""
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route("/places", methods=["GET"],
                 strict_slashes=False)
def places():
    """get all places objects"""
    places = storage.all(Place).values()
    return jsonify([place.to_dict() for place in places]), 200


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def getPlaceCity(city_id):
    """method to get places of a city"""
    city = storage.get(City, city_id)
    places = storage.all(Place).values()
    city.places = [place for place in places if place.city_id == city_id]

    if city is None:
        abort(404)

    return jsonify(city.places.to_dict()), 200


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """method to get place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    return jsonify(place.to_dict()), 200


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """method to delete place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place():
    """method to create a new place"""
    city = storage.get(City, city_id)
    data = request.get_json()
    if city is None:
        abort(404)
    if data is None:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "user_id" is None:
        abort(404)
    if "name" not in data:
        abort(400, "Missing name")
    place = Place(**data)
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """Method to update a place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, val in data.items():
        if key in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            continue
        setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200
