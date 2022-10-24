#!/usr/bin/python3
"""create route for states"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.state import State
from models import storage


@app_views.route("/states", strict_slashes=False,
                 methods=["GET"])
def get_states():
    """Retrieves all states"""
    states = storage.all(States)
    all_states = []
    for state in states.values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["GET"])
def get_a_state(state_id):
    """Retrieve a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())
