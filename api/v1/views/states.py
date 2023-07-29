#!/usr/bin/python3
"""State obj API"""
from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """Get all states or a states whose id is specified"""
    if state_id is None:
        states = storage.all(State).values()
        states_list = [state.to_dict() for state in states]
        return jsonify(states_list)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Create a new state"""
    state = request.get_json()
    if not state:
        abort(400, description="Not a JSON")
    if 'name' not in state:
        abort(400, description="Missing name")
    obj = State(**state)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Update a state object"""
    state = storage.get(State, state_id)
    fixed_data = ['id', 'created_at', 'updated_at']
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in fixed_data:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
