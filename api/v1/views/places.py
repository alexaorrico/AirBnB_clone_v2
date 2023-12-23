#!/usr/bin/python3
"""
    this module contains flask app routes
        flask APP routes:
        methods:
            GET:
                /cities/<city_id>/places:
                    list all city places using city ID
                /places/<place_id>:
                    display place dictionary using ID
            DELETE:
                /places/<place_id>:
                    delete a place using ID
            POST:
                /cities/<city_id>/places:
                    creates a new place to city using city ID
            PUT:
                /places/<place_id>:
                    update place object using ID
"""

from api.v1.views import app_views
from flask import abort, jsonify, request

# import all needed models
from models import storage
from models.city import City
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_city_places(city_id):
    """display all city places using city ID"""
    if (storage.get(City, city_id)) is None:
        abort(404)
    places_list = []
    [places_list.append(place.to_dict())
     for place in storage.all(Place).values()
     if place.city_id == city_id]
    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """diplay a place using ID"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    return obj.to_dict()


@app_views.route("/places/<place_id>", methods=["DELETE"])
def remove_place(place_id):
    """delete a place instance using ID"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """creates a place instance"""
    if (storage.get(City, city_id)) is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    if "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    obj_dict = request.get_json()
    obj_dict["city_id"] = city_id
    obj = Place(**obj_dict)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """update a place instance using ID"""
    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    [setattr(obj, key, value) for key, value in request.get_json().items()
     if key not in ignore_keys]
    obj.save()
    return jsonify(obj.to_dict()), 200
