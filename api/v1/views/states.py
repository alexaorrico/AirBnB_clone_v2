#!/usr/bin/python3
""" Defining State API """

import json
from models import storage
from models.state import State
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import Flask, Blueprint, jsonify, request, url_for, abort


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """ get all sates """

    all_states = storage.all(State).values()
    res = []
    for state in all_states:
        res.append(state.to_dict())
    return jsonify(res)


@app_views.route("/states/<string:state_id>", methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id):
    """ Retrieves states with id """

    res = storage.get(State, state_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route("/states/<string:state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_by_id(state_id):
    """Deletes state by given id"""

    res = storage.get(State, state_id)
    if res is None:
        abort(404)
    storage.delete(res)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'],
                 strict_slashes=False)
def create_state():
    """Adds new state to db"""

    if not request.is_json:
        abort(400, description="Not a JSON")
    res = request.get_json()

    if "name" not in res:
        abort(400, description="Missing name")

    state = State(**res)
    storage.new(state)
    storage.save()
    return state.to_dict(), 201


@app_views.route("/states/<state_id>", methods=['PUT', 'GET'],
                 strict_slashes=False)
def update_state(state_id):
    """ Updates state info """

    res = storage.get(State, state_id)

    if not res:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")
    r_json = request.get_json()

    for idx, idy in r_json.items():
        if idx != "id" and idx != "updated_at" and idx != "created_at":
            setattr(res, idx, idy)
    storage.save()
    return res.to_dict(), 200
