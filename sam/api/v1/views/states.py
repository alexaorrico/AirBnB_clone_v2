#!/usr/bin/python3
""" Handles all default RESTful API action  relating to states """

from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """
    Get all states from the storage and return them as a JSON response.

    Returns:
            - A JSON response containing a list of all states.
            - A status code of 200 if the request was successful.
    """
    states = storage.all("State")
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list), 200


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """
    Get a state by its ID.

    :param state_id: The ID of the state to retrieve.
    :return: A JSON response containing the state information.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404, description="State not found")
    return jsonify(state.to_dict()), 200


@app_views.route(
    '/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes a state from the database.

    :param state_id: The ID of the state to be deleted.
    :type state_id: int
    :return: A JSON response indicating the success of the deletion.
    :rtype: dict
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state():
    """
    Creates a new state.

    Parameters:
    - None

    Returns:
    - A JSON response containing the newly created state.

    Raises:
    - 400 Bad Request if the request is not a JSON or
    if the 'name' field is missing.
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def put_state(state_id):
    """
    Update a state by its ID.

    :param state_id: The ID of the state to update.
    :type state_id: int
    :return: A JSON response containing the updated state.
    :rtype: dict
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
