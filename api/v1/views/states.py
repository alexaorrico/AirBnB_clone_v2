#!/usr/bin/python3
""" This module handles the HTTP methods of a state object"""
from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views

all_states = storage.all('State')
states = []

for state in all_states.values():
    states.append(state.to_dict())


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Handles HTTP request of all the state object """
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def get_state(state_id):
    """ Handles HTTP requests of a single state object """
    state = [state for state in states if state['id'] == state_id]
    if len(state) == 0:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    return jsonify(state)
