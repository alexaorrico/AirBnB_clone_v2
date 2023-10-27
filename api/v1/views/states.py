#!/usr/bin/python3
"""api states"""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
import json


@app_views.route("/states", methods=["GET"])
def get_states():
    """retrieves all State object"""
    allStates = storage.all(State).values()
    statesList = []
    for state in allStates:
        statesList.append(state.to_dict())
    response = make_response(json.dumps(statesList), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/states/<id>", methods=["GET"])
def get_state(id):
    """retrieves State object with id"""
    state = storage.get(State, id)
    if not state:
        abort(404)
    response_data = state.to_dict()
    response = make_response(json.dumps(response_data), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/states/<id>", methods=["DELETE"])
def delete_state(id):
    """delets state with id"""
    state = storage.get(State, id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    res = {}
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/states", methods=["POST"])
def create_state():
    """inserts state if its valid json amd has correct key"""
    abortMSG = "Not a JSON"
    missingMSG = "Missing name"
    if not request.get_json():
        abort(400, description=abortMSG)
    if "name" not in request.get_json():
        abort(400, description=missingMSG)
    data = request.get_json()
    instObj = State(**data)
    instObj.save()
    res = instObj.to_dict()
    response = make_response(json.dumps(res), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/states/<id>", methods=["PUT"])
def put_state(id):
    """update a state by id"""
    abortMSG = "Not a JSON"
    state = storage.get(State, id)
    ignoreKeys = ["id", "created_at", "updated_at"]
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description=abortMSG)
    data = request.get_json()
    for key, value in data.items():
        if key not in ignoreKeys:
            setattr(state, key, value)
    storage.save()
    res = state.to_dict()
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response
