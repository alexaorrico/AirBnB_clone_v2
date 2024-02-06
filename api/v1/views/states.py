#!/usr/bin/python3
"""Handles all default RESTful API actions for State objects."""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import State
from models import storage

# Route for retrieving all State objects
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State objects."""
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)

# Route for retrieving a specific State object by ID
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object."""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)

# Route for deleting a specific State object by ID
@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object."""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

# Route for creating a new State object
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State object."""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201

# Route for updating an existing State object by ID
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object."""
    state = storage.get(State, state_id)
    if state:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
