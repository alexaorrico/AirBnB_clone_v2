#!/usr/bin/python
"""
The states module
"""
from models.engine import db_storage
from flask import Blueprint, jsonify, request, abort
from models.state import State

state_bp = Blueprint('states', __name__, url_prefix='/api/v1/states')


@state_bp.route('/', methods=['GET'], strict_slashes=False)
def get_states():
    states = [state.to_dict() for state in db_storage.all(State).values()]
    return jsonify(states)


@state_bp.route('/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    state = db_storage.get(State, state_id)
    if state is None:
        abort(404)
        return jsonify(state.to_dict())


@state_bp.route('/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    state = db_storage.get(State, state_id)
    if state is None:
        abort(404)
    db_storage.delete(state)
    db_storage.save()
    return jsonify({})


@state_bp.route('/', methods=['POST'], strict_slashes=False)
def create_state():
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    if 'name' not in data:
        abort(400, description='Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@state_bp.route('/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    state = db_storage.get(State, state_id)
    if state in None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
