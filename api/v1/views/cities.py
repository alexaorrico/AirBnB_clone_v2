#!/usr/bin/python3
"""Defines all routes for the `City` entity
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage, classes


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities(state_id):
    """Returns all cities linked to given state_id"""
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        return abort(404)
    cities = state_obj.cities
    if cities is None:
        return abort(404)
    city_objs = []
    for city in cities:
        city_objs.append(city.to_dict())
    return jsonify(city_objs)


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """Returns city with given city_id"""
    city = storage.get("City", city_id)
    if city is None:
        return abort(404)
    return jsonify(city.to_dict())


@app_views.route("states/<state_id>/cities/", methods=["POST"])
def create_city(state_id):
    """Creates a new city in storage"""
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, description="Not a JSON")
    if "name" not in data:
        return abort(400, description="Missing name")
    state = storage.get("State", state_id)
    if state is None:
        return abort(404)
    city = classes["City"](**data)
    state.cities.append(city)
    state.save()
    city.__delattr__("state")
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Deletes a city object from storage"""
    city = storage.get("City", city_id)
    if city is None:
        return abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """Update a city object by id"""
    city = storage.get("City", city_id)
    if city is None:
        return abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, description="Not a JSON")

    data.pop("id", None)
    data.pop("updated_at", None)
    data.pop("created_at", None)

    for k, v in data.items():
        setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict())
