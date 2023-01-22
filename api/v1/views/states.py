#!/usr/bin/python3
"""ALX SE Flask Api State Module."""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def get_states():
    """Return list of all states."""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states), 200


@app_views.route('/states/<string:state_id>', strict_slashes=False)
def get_state(state_id: str):
    """Return a state given its id or 404 when not found."""
    if not state_id:
        abort(404)
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route(
        '/states/<string:state_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_state(state_id: str):
    """Delete a state given its id or 404 when not found."""
    if not state_id:
        abort(404)
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new state."""
    try:
        obj = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if 'name' not in obj:
        abort(400, "Missing name")
    state = State(**obj)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route(
        '/states/<string:state_id>',
        methods=['PUT'],
        strict_slashes=False)
def update_state(state_id: str = None):
    """Update a state given its id."""
    if not state_id:
        abort(404)
    try:
        obj = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for key, value in obj.items():
        if key not in ('id', 'updated_at', 'created_at'):
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
