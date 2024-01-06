#!/usr/bin/python3
"""Defines all the state routes"""

from flask import jsonify, request, abort
from api.v1.views import state_view
from models import storage
from models.state import State


@state_view.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects (collection)"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@state_view.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object (item)"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@state_view.route('/states/<state_id>', methods=['DETELE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@state_view.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State object"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@state_view.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
