#!/usr/bin/python3
"""VIew for States"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.state import State

@app_views.route('/states', methods=['GET'])
def get_states():
    """Return all states"""

    dict_states = storage.all(State)
    states = []
    for state in dict_states.values():
        states.append(state.to_dict())
    return jsonify(states)