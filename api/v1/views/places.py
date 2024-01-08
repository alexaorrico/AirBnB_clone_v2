#!/usr/bin/python3
"""
handles all default RESTFul API actions for Place objects
"""
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                    strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get("City", city_id)
    if city:
        places = []
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    place = storage.get("Place", place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                    strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place = storage.get("Place", place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                    strict_slashes=False)
def create_place(city_id):
    """ Creates a Place """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")
    user = storage.get("User", request.get_json()["user_id"])
    if not user:
        abort(404)
    if "name" not in request.get_json():
        abort(400, "Missing name")
    place = Place(**request.get_json())
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
