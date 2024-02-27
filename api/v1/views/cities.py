#!/usr/bin/python3
"""
view for City objects that handles all default RESTFul API actions
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state_obj = storage.get("State", str(state_id))
    if state_obj is None:
        abort(404)
    all_cities = state_obj.cities
    result = list(all_cities)

    return jsonify(result), 200


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city_obj = storage.get("City", str(city_id))
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict()), 200


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city_obj = storage.get("City", str(city_id))
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return ({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """Creates a city"""
    state_obj = storage.get("State", str(state_id))
    if state_obj is None:
        abort(404)
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, "Not a JSON")
    if "name" not in city_json:
        abort(400, "Missing name")
    city_json["state_id"] = state_id
    city_inst = City(**city_json)
    city_inst.save()
    return jsonify(city_inst.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city_obj = storage.get("City", str(city_id))
    city_json = request.get_json(silent=True)
    if city_obj is None:
        abort(404)
    if city_json is None:
        abort(400, "Not a JSON")
    for key, value in city_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city_obj, key, value)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
