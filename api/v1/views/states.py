#!/usr/bin/python3
from flask import jsonify, abort
from models import storage
from models.state import State
from api.v1.views import app_views

all_states = storage.all('State')
states = []

for state in all_states.values():
    states.append(state.to_dict())

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def get_state(state_id):
    state = [state for state in states if state['id'] == state_id]
    if len(state) == 0:
        abort(404)
    return jsonify(state[0])
