#!/usr/bin/python3

from flask import Flask, jsonify, abort, request
from modles import storage
from models.state import State
from api.vi.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retreive the list of all states objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slasheds=False)
def get_state(state_id):
    """Retrieve the specific state object by Id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slasheds=False)
def delete_state(state_id):
    """Delete a State object by ID"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slasheds=False)
def create_state():
    """Create a new state object"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slasheds=False)
def update_state(state_id):
    """Update a State Object by ID"""
    if state:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a Json"}), 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)


        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
