#!/usr/bin/python3
"""handles all defaults RESTful API actions for cities"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models import storage


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def get_Places(city_id):
    """retrieves all places of a given state"""
    city = storage.get(City, city_id)
    if city:
        places = storage.all(Place)
        place_list = []

        for place in places.values():
            if place.city_id == city_id:
                city_list.append(place.to_dict())
        return jsonify(place_list)
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_place_id(place_id):
    """retrieves a place based on a given id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place based on its id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def create_place(state_id):
    """creates a new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    if "name" not in data:
        return abort(400, "Missing name")
    if "user_id" not in data:
        return abort(400, "Missing user_id")
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    place = Place()
    place.city_id = city_id
    place.user_id = data["user_id"]
    place.name = data["name"]
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """updates a given place"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
