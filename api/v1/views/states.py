#!/usr/bin/python3
"""
The following script creates a new State objects view,
handling all default RESTful API actions.
"""

from flask import abort, jsonify, request
from models.state import State
from api.v1.views import app_views
from models import storage


# Retrieving all State objects
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getting_all_states():
    """
    This method retrieves the list of all State objects.

    Returns:
        JSON: A list of dictionaries representing State objects.
    """
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


# Retrieving a specific State object by ID
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getting_state(state_id):
    """
    This method retrieves a State object.

    Args:
        state_id (str): The ID of the State.

    Returns:
        JSON: A dictionary representing the State object.

    Raises:
        404: If the State object is not found.
    """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


# Deleting a specific State object by ID
@app_views.route('/states/<state_id>', methods=['DELETE'])
def deleting_state(state_id):
    """
    This method deletes a State object.

    Args:
        state_id (str): The ID of the State.

    Returns:
        JSON: An empty dictionary.

    Raises:
        404: If the State object is not found.
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


# Creating a new State object
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def creating_state():
    """
    This method creates a State object.

    Returns:
        JSON: A dictionary representing the newly created State object.

    Raises:
        400:If the request data is not in JSON format or 'name' key is missing.
    """
    if not request.get_json():
        abort(400, 'Not a JSON')

    kwargs = request.get_json()
    if 'name' not in kwargs:
        abort(400, 'Missing name')

    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201


# Updating an existing State object by ID
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updating_state(state_id):
    """
    This method updates a State object.

    Args:
        state_id (str): The ID of the State.

    Returns:
        JSON: A dictionary representing the updated State object.

    Raises:
        404: If the State object is not found.
        400: If the request data is not in JSON format.
    """
    state = storage.get(State, state_id)
    if state and request.get_json():
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)

        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404 if not state else 400)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    """
    Raises a 404 error.

    Returns:
        JSON: A dictionary with the 'error' key set to 'Not found'.
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    """
    Returns a Bad Request message for illegal requests to the API.

    Returns:
        JSON: A dictionary with the 'error' key set to 'Bad Request'.
    """
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
