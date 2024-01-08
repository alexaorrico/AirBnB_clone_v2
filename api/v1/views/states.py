#!/usr/bin/python3
"""Handles all default RestFul API actions for State objects."""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects."""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """Retrieves a State object by id."""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by id."""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    abort(404)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State."""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object by id."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
