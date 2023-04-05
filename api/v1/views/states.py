#!/usr/bin/python3
"""States API routing"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves all state objects"""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a specific state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'State not found')
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a specific state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'State not found')
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new state object"""
    data = request.get_json()
    if not data:
        abort(400, 'Invalid request: Expecting JSON data')
    if 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a specific state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'State not found')
    data = request.get_json()
    if not data:
        abort(400, 'Invalid request: Expecting JSON data')
    not_updateable = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in not_updateable:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
