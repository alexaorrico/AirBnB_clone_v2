#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API actions
"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort
from models.state import State

@app_views.route("/", methods=["GET"], strict_slashes=False)
def retrieve_states():
    """
    REtrieve states
    """
    states = storage.all(State).values()
    for state in states:
        return jsonify(state.to_dict())

@app_views.route("/states/<int:state_id>", methods=["GET"], strict_slashes=False)
def retrieve_state(state_id):
    """
    Retrieves states using the state id
    """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)
