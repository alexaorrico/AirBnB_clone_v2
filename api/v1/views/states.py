#!/usr/bin/python3
"""RESTful API for State"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.state import State
from models import storage

all_states = storage.all(State)


@app_views.route('/states/', methods=['GET'])
@app_views.route('/states/<string:state_id>', methods=['GET'])
def get_state(state_id=None):
    if state_id:
        state = [state for state in all_states.values() if state.to_dict()['id'] == state_id]
        if len(state) == 0:
            abort(404)
        return state[0].to_dict()
    new_list = []
    state_list = [state for state in all_states.values()]
    for state in state_list:
        new_list.append(state.to_dict())
    return jsonify(new_list)
