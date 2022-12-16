#!/usr/bin/python3
""" state objects handles all default RESTFul API"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states_all():
    """Retrieves the list of all State objects: GET /api/v1/states"""
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states_id(state_id):
    """Retrieves a State object: GET /api/v1/states/<state_id>"""
    states = storage.all("State")
    if states is None:
        abort(404, description="Not found")
    return jsonify(states.to_dict())
