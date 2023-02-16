#!/usr/bin/python3

"""city view module"""

from api.v1.views import (app_views)
from models.city import City
from models.state import State
from flask import jsonify, abort, request
import models


@app_views.route('/states/<state_id>/cities',
                 methods=["GET"], strict_slashes=False)
def cities(state_id):
    """return all the cities"""
    state = models.storage.get(State, state_id)
    if state is None:
        return abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=["GET"], strict_slashes=False)
def get_cities_by_id(city_id):
    """return a city by id or 404"""
    city = models.storage.get(City, city_id)
    if city_id is None:
        return abort(404)
    if city is None:
        return abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """delete city data by idDeletes a state based on the city_id
    ---
    definitions:
      City:
        type: object
      Color:
        type: string
      items:"""
    if city_id is None:
        return abort(404)
    city = models.storage.get(City, city_id)
    if city is None:
        return abort(404)

    models.storage.delete(city)
    return jsonify({})


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def add_city(state_id):
    """add new city"""
    try:
        req_data = request.get_json(force=True)
    except Exception:
        req_data = None

    if req_data is None:
        return "Not a JSON", 400

    if "name" not in req_data.keys():
        return "Missing name", 400
    state = models.storage.get(State, state_id)
    if state is None:
        return abort(404)
    new_city = City(**req_data)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """update city object"""
    try:
        req_data = request.get_json(force=True)
    except Exception:
        req_data = None
    if city_id is None:
        return abort(404)
    city = models.storage.get(City, city_id)
    if city is None:
        return abort(404)
    if req_data is None:
        return "Not a JSON", 400
    for key in ("id", "state_id", "created_at", "updated_at"):
        req_data.pop(key, None)
    for k, v in req_data.items():
        setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
