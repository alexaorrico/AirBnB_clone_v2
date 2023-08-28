#!/usr/bin/python3
""" View for State objects """

from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states/',
                 methods=['GET'])
def get_all_states():
    """ Return all the states"""
    states = storage.all(State)
    list_of_states = []
    for state in states:
        list_of_states.append(states[state].to_dict())
    return jsonify(list_of_states)


@app_views.route('/states/<state_id>',
                 methods=['GET'])
def get_state_by_id(state_id):
    """ Return a state based on state_id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'])
def delete_state(state_id):
    """ Delete a state bases on state_id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/',
                 methods=['POST'])
def create_state():
    """ Create new state"""
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")
    if "name" not in new_state:
        abort(400, "Missing name")
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['PUT'])
def update_state(state_id):
    """ Update an exiting state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    for key, value in body.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
