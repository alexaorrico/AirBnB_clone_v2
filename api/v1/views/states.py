#!/usr/bin/python3
"""states for API routes v1"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


# GET all states
# ============================================================================

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """get all states"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


# GET 1 state
# ============================================================================

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """get state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


# DELETE a state
# ============================================================================

@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """delete state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({}), 200


# CREATE a state
# ============================================================================

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """create new state"""
    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')

    if 'name' not in data:
        abort(400, 'Missing name')

    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


# UPDATE a state
# ============================================================================

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updtae state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    req_json = request.get_json()
    ignore_key = ['id', 'created_at', 'updated_at']

    for key, value in req_json.items():
        if key not in ignore_key:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200
