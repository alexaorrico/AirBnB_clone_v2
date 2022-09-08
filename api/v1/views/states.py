#!/usr/bin/python3
"""
State
"""

from api.v1.app import not_found
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    states = storage.all("State")
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return(jsonify(states_list))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id(state_id):
    state = storage.get(State, id)
    if state is None:
        not_found(404)
    return(jsonify(state.to_dict()))
