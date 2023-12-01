#!/usr/bin/python3
"""
API endpoints for State objects.
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/api/v1/states', methods=['GET'], strict_slashes=False)
def get_state():
    """Retrieves the list of all State objects:"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/api/v1/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_id(state_id):
    """
    Retrieves a State object: GET /api/v1/states/<state_id>
    If the state_id is not linked to any State object, raise a 404 error
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    state_data = request.get_json()
    if state_data is None:
        abort(400, 'Not a JSON')
    if 'name' not in state_data:
        abort(400, 'Missing name')
    new_state = State(**state_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/api/v1/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    state_data = request.get_json()
    if state_data is None:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in state_data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
