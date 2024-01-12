#!/usr/bin/python3
"""creates view for State objects that handles all RESTFull API actions"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """retrieves all state objects"""
    states = storage.all('State').values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """retrieves a state object"""
    states = storage.all('State').values()
    for state in states:
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_state(state_id):
    """deletes a state object"""
    states = storage.all('State').values()
    for state in states:
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return {}
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """adds a state object"""
    data = request.get_json()
    # Use make_response() instead of abort
    if data is None:
        abort(400, 'Not a JSON')
    if not data['name']:
        abort(400, 'Missing name')
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    # return make_reponse(jsonify(new_state.to_dict()), 201)
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """adds a state object"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for k, v in data.items():
        if k not in ('id', 'created_at', 'updated_at'):
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict())
