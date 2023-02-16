#!/usr/bin/python3

"""state view module"""

from api.v1.views import (app_views)
from models.state import State
from flask import jsonify, abort, request
import models


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def states():
    """return all the states"""
    all_states = models.storage.all(State)
    return jsonify([state.to_dict() for state in all_states.values()])


@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def get_states_by_id(state_id):
    """return a state by id or 404"""
    state = models.storage.get(State, state_id)
    if state_id is None:
        return abort(404)
    if state is None:
        return abort(404)

    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """delete state data by id"""
    if state_id is None:
        return abort(404)
    state = models.storage.get(State, state_id)
    if state is None:
        return abort(404)

    models.storage.delete(state)
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def add_state():
    """add new state"""
    try:
        req_data = request.get_json(force=True)
    except Exception:
        req_data = None

    if req_data is None:
        return "Not a JSON", 400

    if "name" not in req_data.keys():
        return "Missing name", 400

    new_state = State(**req_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """update state object"""
    try:
        req_data = request.get_json(force=True)
    except Exception:
        return "Not a JSON", 400
    state = models.storage.get(State, state_id)
    if state is None:
        return abort(404)
    for key in ("id", "created_at", "updated_at"):
        req_data.pop(key, None)
    for k, v in req_data.items():
        setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict())
