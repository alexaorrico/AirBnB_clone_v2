#!/usr/bin/python3
"""states Module"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, jsonify, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    states_list = []
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_by_id(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    request_dict = request.get_json()
    if request_dict is None:
        abort(400, 'Not a JSON')
    if 'name' not in request_dict:
        abort(400, 'Missing name')
    state = State(**request_dict)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    request_dict = request.get_json()
    if request_dict is None:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in request_dict.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
