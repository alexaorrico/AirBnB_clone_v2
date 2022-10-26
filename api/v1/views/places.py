#!/usr/bin/python3
"""
This module contains a view for Places object that handles all default
RESTful API actions(basically CRUD operations)
"""

from flask import abort, jsonify, request, make_response
from models import storage
from api.v1.views import app_views
from models.place import Place


@app_views.route("/places", methods=["GET"], strict_slashes=False)
def get_all_places():
    """ This method gets all instances of place """
    places_list = storage.all("Place")
    all_places = []
    for obj in places_list.values():
        all_places.append(obj.to_dict())
    return jsonify(all_places)


@app_views.route("/places/<user_id>", methods=["GET"], strict_slashes=False)
def get_place_by_id(user_id):
    """ This function gets a place by id """
    places = storage.get("Place", user_id)
    if not places:
        abort(404, "Not found")
    return jsonify(places.to_dict())


@app_views.route(
    "/places/<user_id>", methods=["DELETE"], strict_slashes=False
)
def delete_place_by_id(user_id):
    """ This function deletes a place by id """
    places = storage.get("Place", user_id)
    if not places:
        abort(404, "Not found")
    storage.delete(places)
    storage.save()
    return jsonify(places.to_dict()), 200


@app_views.route("/places", methods=["POST"], strict_slashes=False)
def create_place_by_id():
    """ This function creates a new place """
    new_place = request.get_json()
    if not new_place:
        abort(400, "Not a JSON")
    if "email" not in new_place:
        abort(400, "Email is missing")
    if "password" not in new_place:
        abort(400, "Password is missing")
    places = Place(**new_place)
    storage.new(places)
    storage.save()
    return make_response(places.to_dict(), 201)


@app_views.route("/places/<user_id>", methods=["PUT"], strict_slashes=False)
def update_place_by_id(user_id):
    """ This function updates a place by its id """
    places = storage.get("Place", user_id)
    if not places:
        abort(404, "Not found")
    new_place = request.get_json()
    if not new_place:
        abort(400, "Not a JSON")
    ignore_list = ["id", "email", "created_at", "updated_at"]
    for key, value in new_place.items():
        if key not in ignore_list:
            setattr(places, key, value)
        places.save()
        storage.save()
    return jsonify(places.to_dict()), 200
