#!/usr/bin/python3
"""Objects handle all default REStful APi actions for states"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.state import State
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieves the list of all state objects"""
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)