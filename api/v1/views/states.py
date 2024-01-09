#!/usr/bin/python3
"""This module handles the RESTful API actions for State objects."""

from flask import abort, jsonify, request
from models import storage, State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """
    Retrieve the list of all State objects.

    Returns:
        JSON: List of all State objects in a JSON format.
    """
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieve a specific State object by its ID.

    Args:
        state_id (str): ID of the State object to retrieve.

    Returns:
        JSON: State object details in a JSON format.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Create a new State object.

    Returns:
        JSON: Newly created State object details in a JSON format.
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Update an existing State object.

    Args:
        state_id (str): ID of the State object to update.

    Returns:
        JSON: Updated State object details in a JSON format.
    """
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


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Delete a specific State object by its ID.

    Args:
        state_id (str): ID of the State object to delete.

    Returns:
        JSON: Empty dictionary with a 200 status code upon successful deletion.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    state.delete()
    storage.save()
    return jsonify({}), 200
