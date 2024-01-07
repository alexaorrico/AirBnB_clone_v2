#!/usr/bin/python3
"""RESTful API actions for City objects"""


from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_cities(state_id):
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]

    return jsonify(cities), 200


@app_views.route("/cities/<city_id>", strict_slashes=False)
def get_city(city_id):
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    return jsonify(city.to_dict()), 200


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    req_json = request.get_json()
    if not req_json:
        abort(400, description="Not a JSON")

    if "name" not in req_json:
        abort(400, description="Missing name")

    new_city = City(**req_json)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    city = city = storage.get(City, city_id)

    if city is None:
        abort(404)

    req_json = request.get_json()

    if not req_json:
        abort(400, description="Not a JSON")

    for key, value in req_json.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)

    storage.save()

    return jsonify(city.to_dict())
