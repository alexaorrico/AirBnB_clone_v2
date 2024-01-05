#!/usr/bin/python3
"""view for City objects handles all
   default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def state_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = []
    for city in state.cities:
        data.append(city.to_dict())
    return jsonify(data)


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves City info/object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def new_city(state_id):
    """create a new city"""
    data = request.get_json()
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    data['state_id'] = state_id
    city = City(**data)
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """update city object"""
    data = request.get_json()
    city = storage.get(City, city_id)
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    if city is None:
        abort(404)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
