#!/usr/bin/python3
"""
State objects API routes
"""

from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieve the list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieve a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
        '/states/<state_id>', methods=['DELETE'], strict_slashes=False
        )
def delete_state(state_id):
    """Delete a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a State"""
    if not request.is_json:
        return jsonify({'error': 'Not a JSON'}), 400

    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400

    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.is_json:
        return jsonify({'error': 'Not a JSON'}), 400

    data = request.get_json()
    # Ignoring keys that should not be updated
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
