#!/usr/bin/python3
"""Handles RESTful API actions for State objects."""
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieve list of all State objects."""
    states = []
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieve a specific State object by ID."""
    state = None
    if state is None:
        abort(404)
    return jsonify(state)
