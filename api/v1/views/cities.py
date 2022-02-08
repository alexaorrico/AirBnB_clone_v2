#!/usr/bin/python3
"""cities routes module"""
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, make_response, abort, request
from models import storage

model = "City"
parent_model = "State"


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["GET"])
def retrieve_cities(state_id):
    """[GET] Retrieves a list of all City objects linked to a state"""
    return retrieve_models(parent_model, state_id, "cities")


@app_views.route("/cities/<city_id>", methods=["GET"])
def retrieve_city(city_id):
    """[GET] Retrieves a list of all City objects"""
    return retrieve_model(model, city_id)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def del_city(city_id):
    """[DELETE] - deletes a city object with specified id"""
    return del_model(model, city_id)


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["POST"])
def create_city(state_id):
    """[POST] - adds a city object"""
    required_data = {"name"}
    return create_model(model, parent_model, state_id, required_data)


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """[PUT] - updates a city object"""
    auto_data = ["id", "created_at", "updated_at"]
    return update_model(model, city_id, auto_data)
