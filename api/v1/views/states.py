#!/usr/bin/python3
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage, State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects.

    Returns:
        A JSON response containing a list of dictionaries, each representing a State object.
    """
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object.

    Args:
        state_id (str): The ID of the State object to retrieve.

    Returns:
        A JSON response containing a dictionary representing the State object with the given ID.

    Raises:
        404: If no State object with the given ID is found.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object.

    Args:
        state_id (str): The ID of the State object to delete.

    Returns:
        An empty JSON response with a status code of 200.

    Raises:
        404: If no State object with the given ID is found.
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
    Creates a State object.

    Returns:
        A JSON response containing a dictionary representing the newly created State object.

    Raises:
        400: If the HTTP body request is not valid JSON or if the dictionary doesn't contain the 'name' key.
    """
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    state = State(**request.json)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object.

    Args:
        state_id (str): The ID of the State object to update.

    Returns:
        A JSON response containing a dictionary representing the updated State object.

    Raises:
        404: If no State object with the given ID is found.
        400: If the HTTP body request is not valid JSON.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    ignore_keys = {'id', 'created_at', 'updated_at'}
    for key, value in request.json.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
