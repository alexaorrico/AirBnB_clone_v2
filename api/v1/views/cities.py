#!/usr/bin/python3
"""Cities module"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, request, abort


@app_views.route(
    "/states/<state_id>/cities",
    methods=["GET"],
    strict_slashes=False)
def get_all_cities(state_id):
    """Gets all City objects of a State"""
    if storage.get(State, state_id) is None:
        abort(404)
    return (jsonify(([city.to_dict() for city in storage.all(City).values()
                      if city.state_id == state_id])))


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city_id(city_id):
    """Retrieves a City object"""
    if storage.get(City, city_id) is None:
        abort(404)
    else:
        return (jsonify(storage.get(City, city_id).to_dict()))


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Deletes a City object"""
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    else:
        storage.delete(cities)
        storage.save()
        return (jsonify({})), 200


@app_views.route(
    "/states/<state_id>/cities",
    methods=["POST"],
    strict_slashes=False)
def post_city(state_id):
    """Creates a new city object"""
    if storage.get(State, state_id) is None:
        abort(404)
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"})), 400
    if "name" not in request.get_json():
        return (jsonify({"error": "Missing name"})), 400
    data = request.get_json()
    data["state_id"] = state_id
    new_city_obj = City(**data)
    new_city_obj.save()
    return jsonify(new_city_obj.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """Updates the city object"""
    data = request.get_json()
    all_the_cities = storage.get(City, city_id)
    if all_the_cities is None:
        abort(404)
    if not data:
        return (jsonify({"error": "Not a JSON"})), 400
    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(all_the_cities, key, value)
    storage.save()
    return jsonify(all_the_cities.to_dict()), 200
