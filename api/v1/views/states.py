#!/usr/bin/python3
"""a module as states API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def get_states():
    """a function to retrieve all states"""
    states = []
    all_states = storage.all("State").values()
    for state in all_states:
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route("/states/<state_id>")
def get_state(state_id):
    """a function to get a state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    """a function to delete a State object by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def post_state():
    """a function to create a new State object"""
    try:
        json_req = request.get_json()
    except Exception:
        json_req = None

    if not json_req:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in json_req:
        return jsonify({"error": "Missing name"}), 400

    state = State(**json_req)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'])
def update_state(state_id):
    """a function to update a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    try:
        json_req = request.get_json()
    except Exception:
        json_req = None

    if not json_req:
        return jsonify({"error": "Not a JSON"}), 400

    ignored_keys = ["id", "created_at", "updated_at"]
    for key, value in json_req.items():
        if key not in ignored_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
