#!/usr/bin/python3
"""
View for State objects that will handle all default
RESTful API actions
"""
#Allison Edited 11/20 2:43 PM
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_respone, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """retrieves the list of all State objects"""
    all_states = storage.all(State).values()
    states_list = []
    for state in all_states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_by_id(state_id):
    """retrieves a state object when a specific state ID is provided
        will return 404 error if state is not found."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """deletes state object specified by state id, returns a 404 error
        if state is not found, returns empty dictionary with status code 200"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    
