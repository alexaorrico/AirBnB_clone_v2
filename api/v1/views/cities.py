#!/usr/bin/python3
"""Module cities"""
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import *


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    list_cities = []
    state = storage.get(State, state_id)
    if not state:
        return make_response(jsonify({"error": "Not found"}), 404)
    for city in state.cities:
        list_cities.append(city.to_dict())
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if not city:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def delete_city(city_id=None):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if not city:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["POST"])
def post_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    data = request.get_json(force=True, silent=True)
    if not state:
        return make_response(jsonify({"error": "Not found"}), 404)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    s = City(**data)
    s.state_id = state.id
    s.save()
    return make_response(jsonify(s.to_dict()), 201)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def put_city(city_id=None):
    """Updates a City object"""
    city = storage.get(City, city_id)
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignore_keys = ["id", "state_id", "created_at", "updated_at"]
    if not city:
        return make_response(jsonify({"error": "Not found"}), 404)
    else:
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
