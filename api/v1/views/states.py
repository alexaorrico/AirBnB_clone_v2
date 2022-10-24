#!/usr/bin/python3
"""create route for states"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.state import State
from models import storage


@app_views.route("/states", strict_slashes=False,
                 methods=["GET"])
@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["GET"])
def get_states(state_id=None):
    """Retrieves all states"""
    if not state_id:
        states = storage.all(States)
        all_states = []
        for state in states.values():
            all_states.append(state.to_dict())
        return jsonify(all_states)
    else:
        state = storage.get(state_id)
        if not state:
            abort(404)
        return jsonify(state.to_dict())
