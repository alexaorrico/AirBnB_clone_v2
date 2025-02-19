#!/usr/bin/python3
"""State"""
from flask import jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route("/states", methods=["GET"],
                 strict_slashes=False)
def get_states():
    data = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(data)


@app_views.route("/states/<state_id>", methods=["GET"],
                 strict_slashes=False)
def get_state(state_id):
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states", methods=["POST"],
                 strict_slashes=False)
def create_state():
    if not request.is_json:
        abort(400, "Not a JSON")
    new_state_data = request.get_json()
    if "name" not in new_state_data:
        abort(400, "Missing name")
    new_state = State(**new_state_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data_to_update = request.get_json()
    for key, value in data_to_update.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)
