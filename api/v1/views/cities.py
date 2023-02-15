#!/usr/bin/python3
"""
This module contains the views for City objects.
"""

from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route("/states/<string:state_id>/cities", methods=["GET"])
def get_cities_by_state(state_id):
    """
    Retrieves the list of all City objects of a State.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<string:city_id>", methods=["GET"])
def get_city(city_id):
    """
    Retrieves a City object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<string:city_id>", methods=["DELETE"])
def delete_city(city_id):
    """
    Deletes a City object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route("/states/<string:state_id>/cities", methods=["POST"])
def create_city(state_id):
    """
    Creates a City.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "name" not in data:
        abort(400, description="Missing name")
    city = City(**data)
    city.state_id = state_id
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<string:city_id>", methods=["PUT"])
def update_city(city_id):
    """
    Updates a City object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict())
