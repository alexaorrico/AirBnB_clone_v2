#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API actions
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places_of_city(city_id):
    """Retrieves the list of all Place objects of a city"""
    city_obj = storage.get("City", str(city_id))
    if city_obj is None:
        abort(404)
    all_places = city_obj.places
    result = [place.to_dict() for place in all_places]
    return jsonify(result), 200


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_places(place_id):
    """Retrieves a Place object"""
    place_obj = storage.get("Place", str(place_id))
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict()), 200


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes an Place object"""
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return ({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a place"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    dict_ = request.get_json(silent=True)
    if dict_ is None:
        abort(400, "Not a JSON")
    user = storage.get("User", dict_["user_id"])
    if user is None:
        abort(404)
    if "user_id" not in dict_:
        abort(400, "Missing user_id")
    if "name" not in dict_:
        abort(400, "Missing name")

    dict_["city_id"] = city_id
    place = Place(**dict_)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates an Place object"""
    place_obj = storage.get("Place", str(place_id))
    place_dict = request.get_json(silent=True)
    if place_obj is None:
        abort(404)
    if place_dict is None:
        abort(400, "Not a JSON")
    for key, val in place_dict.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place_obj, key, val)
    place_obj.save()
    return jsonify(place_obj.to_dict()), 200
