#!/usr/bin/python3
"""
view for the states
"""

from flask import abort, request, make_response, jsonify
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves all state objects"""
    all_states = storage.all('State')
    all_states = [obj.to_dict() for obj in all_states.values()]
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves state objects by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete state by id"""
    try:
        state = storage.get(State, state_id)
        state.delete()
        storage.save()
    except Exception:
        abort(404, 'Not found')
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Post new state object"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")

    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return make_response(new_state.to_dict(), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update the state object with the provided id"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    ignore_keys = ['id', 'created_id', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return make_response(state.to_dict(), 200)
