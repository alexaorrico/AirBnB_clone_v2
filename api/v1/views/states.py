#!/usr/bin/python3
"""A new view for state objects that handles all default
RESTFUL API actions"""


from flask import Flask, jsonify, request, abort
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves all State objects"""
    all_states = [st.to_dict() for st in storage.all(State).values()]
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """Retrievers a state given it's id"""
    state = storage.get(State, state_id)
    return jsonify(state.to_dict()) if state else abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_states(state_id):
    """Delete a state object given it's id"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State object"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a state obj given it's id"""
    state = storage.get(State, state_id)
    if state:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        keep = ["id", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in keep:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
