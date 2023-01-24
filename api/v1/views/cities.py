#!/usr/bin/python3
from models import storage
from models.state import State
from models.city import City
from . import app_views
from flask import jsonify, abort, request

@app_views.route("/states/<state_id>/cities")
def cities(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    city_list = []
    for city in cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)

@app_views.route("/cities/<city_id>")
def city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})

@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if "name" not in data:
        abort(400, "Missing name")
    data["state_id"] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201

@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if "id" in data:
        data.pop("id")
    if "created_at" in data:
        data.pop("created_at")
    if "updated_at" in data:
        data.pop("updated_at")
    if "state_id" in data:
        data.pop("state_id")
    for key, value in data.items():
        city.__setattr__(key, value)
    city.save()
    return jsonify(city.to_dict())