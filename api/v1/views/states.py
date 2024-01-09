#!/usr/bin/python3
"""
Create a new view for State objects - handles all default RESTful API actions.
"""

# Import necessary modules
from flask import abort, jsonify, request
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """
    Retrieves the list of all State objects.

    Returns:
        JSON: List of all State objects in a JSON format.
    """
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object by ID.

    Args:
        state_id (str): ID of the State object.

    Returns:
        JSON: State object details in JSON format if found, else 404 error.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes a State object by ID.

    Args:
        state_id (str): ID of the State object to delete.

    Returns:
        JSON: Empty dictionary with a 200 status code.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a new State object.

    Returns:
        JSON: created State object details in JSON format with 201 status code.
    """
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object by ID.

    Args:
        state_id (str): ID of the State object to update.

    Returns:
        JSON: Updated State object in JSON format with a 200 status code.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200


@app_views.errorhandler(404)
def not_found(error):
    """
    Handles 404 errors.

    Returns:
        JSON: Error message for 404 status code.
    """
    return jsonify({"error": "Not found"}), 404


@app_views.errorhandler(400)
def bad_request(error):
    """
    Handles 400 errors.

    Returns:
        JSON: Error message for 400 status code.
    """
    return jsonify({"error": "Bad request"}), 400
