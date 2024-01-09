#!/usr/bin/python3
"""Module for handling RESTful API actions for State objects.

This module defines routes and actions for handling State objects
based on the RESTful API conventions.

Routes:
    - GET /api/v1/states
    - GET /api/v1/states/<state_id>
    - DELETE /api/v1/states/<state_id>
    - POST /api/v1/states
    - PUT /api/v1/states/<state_id>

"""

from flask import Blueprint
from flask import jsonify
from flask import request
from models import storage
from models.state import State
from api.v1.app import not_found


app_views = Blueprint('app_views', __name__)


@app_views.route('/api/v1/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects."""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/api/v1/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object by state_id."""
    state = storage.get(State, state_id)
    if state is None:
        not_found(404)
    return jsonify(state.to_dict())


@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by state_id."""
    state = storage.get(State, state_id)
    if state is None:
        not_found(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State."""
    data = request.get_json()
    if not data:
        not_found(400, 'Not a JSON')
    if 'name' not in data:
        not_found(400, 'Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/api/v1/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object by state_id."""
    state = storage.get(State, state_id)
    if state is None:
        not_found(404)
    data = request.get_json()
    if not data:
        not_found(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
