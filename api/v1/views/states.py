#!/usr/bin/python3
"""VIew for States"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.state import State
from flask import abort


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_states():
    """Return all states"""
    dict_states = storage.all(State)
    states = []
    for state in dict_states.values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_states(state_id):
    """Return state according class and id of state
        or return Error: Not found if it doesn't exist.
    """
    if state_id:
        dict_state = storage.get(State, state_id)
        if dict_state is None:
            abort(404)
        else:
            return jsonify(dict_state.to_dict())
