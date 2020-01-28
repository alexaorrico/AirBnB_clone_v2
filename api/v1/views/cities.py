#!/usr/bin/python3
from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.city import City


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """retrieves all city objects based on state_id"""
    city_list = []
    if storage.get('State', state_id) is None:
        abort(404)
    cities = storage.all('City').values()
    for city in cities:
        if city.state_id == state_id:
            city_list.append(city.to_dict())
    return (jsonify(city_list))


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """retrieves a single city object"""
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404)
    else:
        return (jsonify(city_obj.to_dict()))


@app_views.route("/cities/<city_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes a city by ID"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return (jsonify({})), 200


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"],
                 strict_slashes=False)
def post_city(state_id):
    """create a city"""
    if storage.get("State", state_id) is None:
        abort(404)
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"})), 400
    if "name" not in request.get_json():
        return (jsonify({"error": "Missing name"})), 400
    json_dict = request.get_json()
    json_dict["state_id"] = state_id
    new_city = City(**json_dict)
    new_city.save()
    return (jsonify(new_city.to_dict())), 201


@app_views.route("/cities/<city_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """updates a city object"""
    ignore = ["id", "state_id", "created_at", "updated_at"]
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"})), 400
    for k, v in request.get_json().items():
        if k not in ignore:
            setattr(city, k, v)
    storage.save()
    return (jsonify(city.to_dict())), 200
