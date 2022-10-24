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
    states = storage.all(State)
    all_states = []
    for state in states.values():
        all_states.append(state.to_dict())
    return jsonify(all_states)
