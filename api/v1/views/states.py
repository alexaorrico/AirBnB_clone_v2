#!/usr/bin/python3
"""
    API view related to State objects that handles all the default
    actions.
"""
import requests
from api.v1.views import app_views
from models import storage
from models.state import State
import json
from werkzeug.exceptions import BadRequest, NotFound
from flask import Flask, request, jsonify, make_response, abort


def __is_valid_json(data):
    """
    Checks if the given data is a valid json.

    Args:
        data : Data to check

    Returns:
        True: If data is a valid json.
        False: If data is not a valid json.
    """
    try:
        json.loads(data)

        return True
    except Exception:
        return False


@app_views.route('/states', methods=['GET'])
def list() -> json:
    """
    Retrieves the list of all State objects.

    Returns:
        json: List of State objects with status code 200.
    """
    states = storage.all(State)
    list = []
    for key, state in states.items():
        list.append(state.to_dict())
    return make_response(jsonify(list), 200)


@app_views.route('/states/<state_id>', methods=['GET'])
def show(state_id) -> json:
    """
    Retrieves a specified State object.

    Args:
        state_id : ID of the wanted State object.

    Raises:
        NotFound: Raises a 404 error if state_id
        is not linked to any State object.

    Returns:
        json: Wanted State object with status code 200.
    """
    state = storage.get(State, state_id)

    if state is None:
        raise NotFound

    return make_response(jsonify(state.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete(state_id) -> json:
    """
    Deletes a specified State object.

    Args:
        state_id : ID of the wanted State object.

    Raises:
        NotFound: Raises a 404 error if state_id
        is not linked to any State object.

    Returns:
        json: Empty dictionary with the status code 200.
    """
    state = storage.get(State, state_id)

    if state is None:
        raise NotFound

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/', methods=['POST'])
def create() -> json:
    """
    Creates a new State object.

    Error cases:
        BadRequest: If the given data is not a
        valid json or if the key 'name' is not
        present sends status code 400.

    Returns:
        json: The new State with the status code 201.
    """
    data = request.get_data()

    if not __is_valid_json(data):
        return make_response('Not a JSON', 400)

    data = json.loads(data)

    if 'name' not in data.keys():
        return make_response('Missing name', 400)

    state = State(data)
    for key, value in data.items():
        state.__setattr__(key, value)
    storage.new(state)
    storage.save()

    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update(state_id) -> json:
    """
    Update a specified State object.

    Args:
        state_id : Id of the wanted State object.

    Returns:
        json: The updated State object with the status code 200.
    """
    data = request.get_data()

    if not __is_valid_json(data):
        return make_response('Not a JSON', 400)

    data = json.loads(data)
    state = storage.get(State, state_id)

    if state is None:
        raise NotFound

    for key, value in data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            state.__setattr__(key, value)

    storage.new(state)
    storage.save()

    return make_response(jsonify(state.to_dict()), 200)
