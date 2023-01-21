#!/usr/bin/python3
"""ALX SE Flask Api State Module."""
from api.v1.views import state_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@state_views.route('/', strict_slashes=False)
def get_states():
    """Return list of all states."""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states), 200


@state_views.route('/<string:state_id>', strict_slashes=False)
def get_state(state_id: str = None):
    """Return a state given its id or 404 when not found."""
    if not state_id:
        abort(404)
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict()), 200


@state_views.route(
        '/<string:state_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_state(state_id: str = None):
    """Delete a state given its id or 404 when not found."""
    if not state_id:
        abort(404)
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    return jsonify({}), 200


@state_views.route('/', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new state."""
    try:
        obj = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if 'name' not in obj:
        abort(400, "Missing name")
    state = State(**obj)
    state.save()
    return jsonify(state.to_dict()), 201


@state_views.route('/<string:state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id: str = None):
    """Update a state given its id."""
    if not state_id:
        abort(404)
    try:
        obj = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if 'name' not in obj:
        abort(400, "Missing name")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.name = obj['name']
    state.save()
    return jsonify(state.to_dict()), 200
