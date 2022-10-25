#!/usr/bin/python3
"""This module retrieves state objects
"""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_state():
    """This method gets all instances of state"""
    states_list = storage.all("State")
    all_states = []
    for obj in states_list.values():
        all_states.append(obj.to_dict())
    return jsonify(all_states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state_by_id(state_id):
    """This function get the state by its id."""
    state = storage.get("State", state_id)
    if not state:
        abort(404, "Not found")
    return jsonify(state.to_dict())


@app_views.route(
    "/states/<state_id>", methods=["DELETE"], strict_slashes=False
    )
def delete_state_by_id(state_id):
    """This function delete_state_by_id"""
    state = storage.get("State", state_id)
    if not state:
        abort(404, "Not found")
    storage.delete(state)
    storage.save()
    return jsonify(state.to_dict()), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state_by_id():
    """This function creates a new state"""
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")
    if "name" not in new_state:
        abort(400, "Name is missing")
    state = State(**new_state)
    storage.new(state)
    storage.save
    return make_response(state.to_dict(), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state_by_id(state_id):
    """This function updates state by its id."""
    state = storage.get("State", state_id)
    if not state:
        abort(404, "Not found")
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")
    ignore_list = ["id", "created_at", "updated_at"]
    for key, value in new_state.items():
        if key not in ignore_list:
            setattr(state, key, value)
        state.save()
        storage.save()
    return jsonify(state.to_dict()), 200
