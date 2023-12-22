#!/usr/bin/python3
"""
    this module contains flask app routes
        flask APP routes:
        methods:
            GET:
                /states/<state_id>/cities:
                    list all state cities using state ID
                /cities/<city_id>:
                    display city dictionary using ID
            DELETE:
                /cities/<city_id>:
                    delete a city using ID
            POST:
                /states/<state_id>/cities:
                    creates a new city to state using state ID
            PUT:
                /cities/<city_id>:
                    update city object using ID
"""

from api.v1.views import app_views
from flask import abort, jsonify, request

# import all needed models
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_state_cities(state_id):
    """display all state cities using state ID"""
    if (storage.get(State, state_id)) is None:
        abort(404)
    city_list = []
    [city_list.append(city.to_dict())
     for city in storage.all(City).values()
     if city.state_id == state_id]
    return jsonify(city_list)


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """diplay a city using ID"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    return obj.to_dict()


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def remove_city(city_id):
    """delete a city instance using ID"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """creates a new city instance"""
    if (storage.get(State, state_id)) is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    obj_dict = request.get_json()
    obj_dict["state_id"] = state_id
    obj = City(**obj_dict)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """update a city instance using ID"""
    ignore_keys = ["id", "state_id", "created_at", "updated_at"]
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    [setattr(obj, key, value) for key, value in request.get_json().items()
     if key not in ignore_keys]
    obj.save()
    return jsonify(obj.to_dict()), 200
