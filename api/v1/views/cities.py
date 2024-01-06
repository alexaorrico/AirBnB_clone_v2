#!/usr/bin/python3
""" View for citys """

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import abort, jsonify, request


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cities(state_id):
    """ method to get a cities of a state """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    return jsonify([city.to_dict() for city in state.cities]), 200


@app_views.route("/api/v1/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    """ method to get city id"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    return jsonify(city.to_dict()), 200


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """ method to delete city """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """ method to create a new state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    city = City(**data)
    setattr(city, 'state_id', state_id)
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """ Method to update a city """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, val in data.items():
        if key == "id" or key == "created_at" or key == "updated_at":
            continue
        setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
