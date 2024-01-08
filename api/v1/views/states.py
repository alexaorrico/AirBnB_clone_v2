#!/usr/bin/python3
"""State view module"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """Retrieves the list of all State objects"""
    state_list = storage.all(State).values()
    state_dict = []

    for state in state_list:
        state_dict.append(state.to_dict())

    return jsonify(state_dict)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a state based on it's ID"""
    state = storage.get(State, state_id)

    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state based on it's ID"""
    state = storage.get(State, state_id)

    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """Adds a state"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updates a state"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if (key == "id" or key == "created_at" or key == "updated_at"):
            pass
        else:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200
