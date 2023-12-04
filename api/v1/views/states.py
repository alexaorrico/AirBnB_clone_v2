#!/usr/bin/python3
""" State API """

import json
from models import storage
from models.state import State
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import Flask, Blueprint, jsonify, request, url_for, abort


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves all states """

    all_states = storage.all(State).values()
    result = []
    for state in all_states:
        result.append(state.to_dict())
    return jsonify(result)


@app_views.route("/states/<string:state_id>", methods=['GET'],
                 strict_slashes=False)
def get_state_id(state_id):
    """ Gets states using id """

    result = storage.get(State, state_id)
    if result is None:
        abort(404)
    return jsonify(result.to_dict())


@app_views.route("/states/<string:state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_id(state_id):
    """Deletes state of specified id"""

    result = storage.get(State, state_id)
    if result is None:
        abort(404)
    storage.delete(result)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'],
                 strict_slashes=False)
def create_state():
    """Create new state to db"""

    if not request.is_json:
        abort(400, description="Not a JSON")
    result = request.get_json()

    if "name" not in result:
        abort(400, description="Missing name")

    state = State(**result)
    storage.new(state)
    storage.save()
    return state.to_dict(), 201


@app_views.route("/states/<state_id>", methods=['PUT', 'GET'],
                 strict_slashes=False)
def update_state(state_id):
    """ Update State using id """

    result = storage.get(State, state_id)

    if not result:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")
    r_json = request.get_json()

    for idx, idy in r_json.items():
        if idx != "id" and idx != "updated_at" and idx != "created_at":
            setattr(result, idx, idy)
    storage.save()
    return result.to_dict(), 200
