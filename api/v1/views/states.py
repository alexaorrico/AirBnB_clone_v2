#!/usr/bin/python3
"""Flask Api State module"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'],
                 strict_slashes=False)
def states():
    """Retrieve all states"""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states), 200


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Retrieve a state based on its state_id or return 404 if not found"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a state based on its state_id or return 404 if not found"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """Creates a new state or return 404 if not found"""
    if not request.is_json:
        abort(400, "Not a JSON")
    obj = request.get_json()
    if 'name' not in obj:
        abort(400, "Missing name")
    state = State(**obj)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id: str = None):
    """Update a state given its id or return 404 if not found"""
    if not request.is_json:
        abort(400, "Not a JSON")
    obj = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for key, value in obj.items():
        if key not in ('id', 'updated_at', 'created_at'):
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
