#!/usr/bin/python3
"""State view"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route("/states", methods=['GET'], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """get states or one state based on state_id"""
    new_list = []
    key = "States." + str(state_id)
    if state_id is None:
        objs = storage.all(State)
        for key, value in objs.items():
            new_list.append(value.to_dict())
    elif key in storage.all(State).keys():
        return jsonify(storage.all(State)[key].to_dict())
    else:
        abort(404)
    return jsonify(new_list)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """delete state based on the state_id passed"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'],
                 strict_slashes=False)
def create_state():
    """create state"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id=None):
    """Update a state"""
    key = "State." + str(state_id)
    if key not in storage.all(State).keys():
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ["created_at", "updated_at", "id"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
