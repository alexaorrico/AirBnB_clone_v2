#!/usr/bin/python3
"""Routes for the states resource."""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route("/states/", methods=["GET"])
def get_states():
    """Return a list of the states."""
    state_list = storage.all(State)
    state_list = [
        state.to_dict() for state in state_list.values()
    ]
    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """Get a state by id."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Delete a state by id."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route("/states/", methods=["POST"])
def add_state():
    """Create a new state."""
    try:
        state_info = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)
    if "name" not in state_info:
        return make_response("Missing name", 400)
    state = State(**state_info)
    state.save()
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """Update a state by id."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    try:
        state_info = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)
    for key, value in state_info.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
