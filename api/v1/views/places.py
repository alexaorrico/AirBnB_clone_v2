#!/usr/bin/python3
"""Place module"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from flask import jsonify, request, abort


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places_from_city(city_id):
    """Gets all Places objects from a City object"""
    if storage.get(City, city_id) is None:
        abort(404)
    return (jsonify(([place.to_dict() for place in storage.all(Place).
                      values()if place.city_id == city_id])))


@app_views.route("/places/<city_id>", methods=["GET"])
def get_place_id(place_id):
    """Gets a Place object"""
    if storage.get(Place, place_id) is None:
        abort(404)
    return (jsonify(storage.get(Place, place_id).to_dict()))


@app_views.route("places/<place_id>", methods=["DELETE"])
def delete_place(city_id):
    """Deletes a Place object"""
    place_object = storage.get(Place, place_id)
    if place_object is None:
        abort(404)
    else:
        storage.delete(place_object)
        storage.save()
        return (jsonify({})), 200


@app_views.route(
    "/cities/<city_id>/places",
    methods=["POST"],
    strict_slashes=False)
def post_place(city_id):
    """Creates a new place object"""
    if storage.get(City, city_id) is None:
        abort(404)
    data = request.get_json()
    if not data:
        return (jsonify({"error": "Not a JSON"})), 400
    if "user_id" not in data:
        return (jsonify({"error": "Missing user_id"})), 400
    if storage.get(User, data["user_id"]) is None:
        abort(404)
    if "name" not in data:
        return (jsonify({"error": "Missing name"})), 400
    user_id = data["user_id"]
    place_name = data["name"]
    new_place_obj = Place(user_id=user_id, name=name, city_id=city_id)
    for k, v in data.items():
        setattr(new_place_obj, k, v)
    new_place_obj.save()
    return jsonify(new_place_obj.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """Updates the place object"""
    ignore_data = ["id", "user_id", "city_id", "created_at", "updated_at"]
    data = request.get_json()
    all_the_places = storage.get(Place, place_id)
    if all_the_places is None:
        abort(404)
    if not data:
        return (jsonify({"error": "Not a JSON"})), 400
    for key, value in data.items():
        if key not in ignore_data:
            setattr(all_the_places, key, value)
    storage.save()
    return jsonify(all_the_places.to_dict()), 200
