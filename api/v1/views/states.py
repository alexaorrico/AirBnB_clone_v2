#!/usr/bin/python3
"""Create a view for state"""

from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    state_obj = storage.all(State)
    return jsonify([obj.to_dict() for obj in state_obj.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states_id(state_id):
    """Retrieves a State object by ID"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by ID"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new state"""
    new_state = request.get_json()
    if not new_state:
        abort(400, 'Not a JSON')
    if 'name' not in new_state:
        abort(400, 'Missing name')
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object by ID"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    # Update the State object's attributes based on the JSON data
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
