#!/usr/bin/python3
"""Cities Objects actions"""

from api.v1.views import *
from flask import Flask, jsonify
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=['GET'])
def get_cities(state_id):
    """GET Method"""
    return parent_obj(State, state_id, "cities")


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['GET'])
def get_city_id(city_id):
    """"State by id GET Method"""
    if city_id:
        return get_object(City, city_id)


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_city(city_id):
    """Delete a State DELETE Method"""
    return delete(City, city_id)


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=['POST'])
def post_city(state_id):
    """POST Method"""
    return post(City, State, state_id, {"name"})


@app_views.route("/cities/<city_id>", methods=['PUT'])
def put_city(city_id):
    """PUT Method"""
    return put(City, city_id, ["id", "created_at", "updated_at"])
