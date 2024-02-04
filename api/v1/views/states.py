#!/usr/bin/python3
"""
Handles RESTFul API actions for states
"""

from api.v1.views import app_views
from flask import jsonify
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