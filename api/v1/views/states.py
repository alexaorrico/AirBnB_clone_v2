#!/usr/bin/python3
'''states.py'''
from flask import abort, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    '''get states'''
    if state_id:
        state = storage.get(State, state_id)
        if state:
            return jsonify(state.to_dict())
        else:
            abort(404)
    all_states = []
    for state in storage.all('State').values():
        all_states.append(state.to_dict())
    return jsonify(all_states)
