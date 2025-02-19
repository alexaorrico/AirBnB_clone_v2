#!/usr/bin/python3
"""Place"""
from flask import jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import app_views
from models.user import User
from models.place import Place
from models.city import City


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places(city_id):
    """Gets the list of all places"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = [place.to_dict() for place in storage.all(Place).values()
            if place.city_id == city_id]
    return jsonify(data)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a place object"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a place object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    new_place_data = request.get_json()
    if not new_place_data:
        abort(400, "Not a JSON")
    if "user_id" not in new_place_data:
        abort(400, "Missing user_id")
    user = storage.get(User, new_place_data['user_id'])
    if not user:
        abort(404)
    if "name" not in new_place_data:
        abort(400, "Missing name")
    new_place_data['city_id'] = city_id
    new_place = Place(**new_place_data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data_to_update = request.get_json()
    if not data_to_update:
        abort(400, "Not a JSON")
    for key, value in data_to_update.items():
        if key not in ["id", "user_id", "city_id",
                       "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes place object"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)
