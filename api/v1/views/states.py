#!/usr/bin/python3
"""api end point
"""

from flask import jsonify, abort
from api.v1.views import app_views
from models import storage


@app_views.route('/states', strict_slashes=False)
@app_views.route('/states/<state_id>', strict_slashes=False)
def states(state_id=None):
    """display the states and cities listed in alphabetical order"""
    _states = storage.all("State")
    if state_id:
        state_id = 'State.' + state_id
        if state_id not in _states:
            abort(404)
        return jsonify(_states[state_id].to_dict())
    states_list = [state.to_dict() for state in _states.values()]
    return jsonify(states_list)
