#!/usr/bin/python3
"""
New view for State objects
"""

from flask import abort, jsonify, request
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', strict_slashes=False)
def get_states():
    """retrieves all State objects"""
    states = storage.all(State).values()
    states_list = []
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state_id(state_id):
    """retrieves a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
        '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """create a State"""
    response = request.get_json()
    if response is None:
        abort(400, 'Not a JSON')
    if 'name' not in response:
        abort(400, 'Missing name')
    state = State(**response)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update a State obbject"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
