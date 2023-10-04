#!/usr/bin/python3
"""The `states` module"""


from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def list_all_states():
    """Lists all states"""
    state = storage.all(State)
    return jsonify([states.to_dict() for states in state.values()])


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def list_state_id(state_id):
    """Lists states by id"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return make_response(jsonify(state.to_dict()), 404)


@app_views.route("/states/<state_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """Deletes a state by id"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a new state"""
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    if "name" not in payload:
        abort(400, "Missing name")
    new_state = State(**payload)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state_id(state_id):
    """Updates state by id"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    for key, value in payload.items():
        if key not in {"id", "created_at", "updated_at"}:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
