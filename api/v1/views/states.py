#!/usr/bin/python3
"""Modules that handles all Restful API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states_list():
    """Returns collection of all States"""
    states = []
    all_states = storage.all(State).values()
    for state in all_states:
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_by_id(state_id):
    """Returns an object state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a given state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Creates a new given state"""
    new_state = request.get_json()
    if not new_state:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in new_state:
        return jsonify({'error': 'Missing name'}), 400
    else:
        new_obj = State(**new_state)
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a given state"""
    state_to_update = request.get_json()
    if not state_to_update:
        return jsonify({'error': 'Not a JSON'}), 400

    my_dict = storage.get(State, state_id)
    if my_dict:
        for key, value in state_to_update.items():
            setattr(my_dict, key, value)
        storage.save()
        return jsonify(my_dict.to_dict()), 200
    else:
        abort(404)
