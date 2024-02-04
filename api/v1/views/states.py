#!/usr/bin/python3
"""
Handles RESTFul API actions for states
"""

from flask import abort
from api.v1.views import app_views
from flask import jsonify
from flask import request
from models.state import State
from models import storage


@app_views.route("/states", strict_slashes=False)
def all_states():
    """
    Returns list of all states
    """
    states = storage.all("State")
    list_states = []
    for state in states.values():
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def one_state(state_id):
    """
    Returns a state object based on id
    """
    state = storage.get("State", state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Returns a state object based on id
    """
    state = storage.get("State", state_id)
    if state:
        storage.delete(state)
        return jsonify({}), 200
    abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def add_state():
    """
    Adds a state object based on data provided
    """
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, "Missing name")

    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a state object based on data provided
    """
    state = storage.get("State", state_id)
    if state:
        data = request.get_json(silent=True)
        if not data:
            abort(400, "Not a JSON")
        keys_to_ignore = ["created_at", "id", "updated_at"]
        for k, v in data.items():
            if k not in keys_to_ignore:
                state.__dict__.update({k: v})
        storage.save()
        return jsonify(state.to_dict()), 200

    abort(404)
