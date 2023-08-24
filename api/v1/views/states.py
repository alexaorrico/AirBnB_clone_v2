#!/usr/bin/python3
""" View for State objects """

from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage


@app_views.route('/states/', methods=['GET'])
def get_all_states():
    """ Return all the states"""
    states = storage.all(State)
    list_of_states = []
    for state in states:
        list_of_states.append(states[state].to_dict())
    return jsonify(list_of_states)

@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_by_id(state_id):
    """ Return a state based on state_id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Delete a state bases on state_id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200

