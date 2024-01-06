#!/usr/bin/python3
"""
Module for State objects that handles
all default RestFul API actions
"""

from flask import jsonify, Blueprint, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Returns list of all State objects"""
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states), 200


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id):
    """Returns a State object based on state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    states_dictionary = state.to_dict()
    return jsonify(states_dictionary), 200


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object based on state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    answer = request.get_json()
    if answer is None:
        abort(400, 'Not a JSON')
    if 'name' not in answer:
        abort(400, 'Missing name')
    new_state = State(**answer)
    new_state.save()
    state_dictionary = new_state.to_dict()
    return jsonify(state_dictionary), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Updates a State object based on state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    answer = request.get_json()
    if answer is None:
        abort(400, 'Not a JSON')
    for key, value in answer.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    state_dictionary = state.to_dict()
    return jsonify(state_dictionary), 200
