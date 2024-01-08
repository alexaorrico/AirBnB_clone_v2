#!/usr/bin/python3
"""
This module defines the view for State objects that handles all default
RESTFul API actions.
"""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.state import State

app = Flask(__name__)


# Route: /api/v1/states
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State objects."""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


# Route: /api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object by id."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


# Route: /api/v1/states/<state_id>
@app_views.route(
            '/states/<state_id>',
            methods=['DELETE'],
            strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by id."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


# Route: /api/v1/states
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State."""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


# Route: /api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object by id."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
