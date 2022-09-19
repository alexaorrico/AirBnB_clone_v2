#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_get():
    """Retrieves the list of all State"""
    states_list = []
    all_states = storage.all(State)
    for key, value in all_states.items():
        states_list.append(value.to_dict())
    return jsonify(states_list)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def states_post():
    """Creates a State"""
    transform_dict = request.get_json()
    if transform_dict is None:
        abort(400, "Not a JSON")
    if 'name' not in transform_dict.keys():
        abort(400, "Missing name")
    else:
        new_state = State(**transform_dict)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id_get(state_id):
    """Retrieves a State object and 404 if it's an error"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_id_delete(state_id):
    """Deletes a State object and 404 if it's an error"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_id_put(state_id):
    """Updates a State object"""
    ignore_list = ['id', 'created_at', 'updated_at']
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    transform_dict = request.get_json()
    if transform_dict is None:
        abort(400, "Not a JSON")
    for key, value in transform_dict.items():
        if key not in ignore_list:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
