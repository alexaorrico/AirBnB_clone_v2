#!/usr/bin/python3
"""api cities"""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
import json


@app_views.route("/states/<id_state>/cities", methods=["GET"])
def get_cities(id_state):
    """retrieves all cities by state id object"""
    state = storage.get(State, id_state)
    citiesList = []
    if not state:
        abort(404)
    for city in state.cities:
        citiesList.append(city.to_dict())
    res = citiesList
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/cities/<id>", methods=["GET"])
def get_city(id):
    """retrieves cities object with id"""
    city = storage.get(City, id)
    if not city:
        abort(404)
    response_data = city.to_dict()
    response = make_response(json.dumps(response_data), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/cities/<id>", methods=["DELETE"])
def delete_city(id):
    """delets city with id"""
    city = storage.get(City, id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    res = {}
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/states/<id_state>/cities", methods=["POST"])
def create_city(id_state):
    """inserts city if its valid json amd has correct key and state id"""
    missingMSG = "Missing name"
    abortMSG = "Not a JSON"
    state = storage.get(State, id_state)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description=abortMSG)
    if "name" not in request.get_json():
        abort(400, description=missingMSG)
    data = request.get_json()
    instObj = City(**data)
    instObj.state_id = id_state
    instObj.save()
    res = instObj.to_dict()
    response = make_response(json.dumps(res), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/cities/<id>", methods=["PUT"])
def put_city(id):
    """update a city by id"""
    abortMSG = "Not a JSON"
    city = storage.get(City, id)
    ignoreKeys = ["id", "state_id", "created_at", "updated_at"]
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description=abortMSG)
    data = request.get_json()
    for key, value in data.items():
        if key not in ignoreKeys:
            setattr(city, key, value)
    storage.save()
    res = city.to_dict()
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response
