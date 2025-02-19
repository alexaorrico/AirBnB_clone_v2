#!/usr/bin/python3
"""State objects for all RESTFUL API"""


from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves all state objects from storage"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a state object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
        '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deleting a state object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State object"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    data = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")
    keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
