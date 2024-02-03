#!/usr/bin/python3
"""Views for the states"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """Return states"""
    return [state.to_dict() for state in storage.all(State).values()]


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state(state_id):
    """Return a state"""
    state = storage.get(State, state_id)
    if state is None:
        return {"error": "Not found"}, 404
    return state.to_dict()


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a state"""
    state = storage.get(State, state_id)
    if state is None:
        return {"error": "Not found"}, 404
    storage.delete(state)
    storage.save()
    return {}, 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a state"""
    state = request.get_json()
    if state is None:
        return {"error": "Not a JSON"}, 400
    if "name" not in state:
        return {"error": "Missing name"}, 400
    state = State(**state)
    state.save()
    return state.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a state"""
    state = storage.get(State, state_id)
    if state is None:
        return {"error": "Not found"}, 404
    state_data = request.get_json()
    if state_data is None:
        return {"error": "Not a JSON"}, 400
    for key, value in state_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return state.to_dict(), 200
