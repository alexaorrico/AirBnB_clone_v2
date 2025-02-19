#!/usr/bin/python3
"""
Create a new view for City objects
that handles all default RESTFul API actions
"""
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
import json


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all City objects of a State
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities_list = [city.to_dict() for city in state.cities]
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City use POST request"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = City(state_id=state_id, **data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def updata_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    for k, v in data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(city, k, v)

    city.save()
    return make_response(jsonify(city.to_dict()), 200)
