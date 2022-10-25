#!/usr/bin/python3
"""
a new view for User object that handles
all default RESTFul API actions
"""


from api.v1.views import app_views
from models import storage
from models.state import State
from flask import Flask, make_response, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """
    Retrieves the list of all State objects

    Returns:
        json: Wanted States object with status code 200.
    """
    states = storage.all(State)
    list = []

    for state in states.items():
        list.append(state.to__dict())
    return make_response(jsonify(list), 200)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def single_state(state_id):
    """
    Retrieves a specified State object.

    Args:
        state_id : ID of the specified State object.

    Raises:
        NotFound: Raises a 404 error if state_id
        is not linked to any State object.

    Returns:
        json: Wanted State object with status code 200.
    """
    state = storage.get(State, state_id)

    if state is None:
        raise NotFound

    return make_response(jsonify(state.to__dict()), 200)


@app_views.route(
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_state(state_id):
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


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """
    Creates a new State object.

    Error cases:
        BadRequest: If the given data is not a
        valid json or if the key 'name' is not
        present sends status code 400.

    Returns:
        json: The new State with the status code 201.
    """
    state = State(**request.get_json())

    if not request.get_json:
        return make_response('Not a JSON', 400)

    if 'name' not in request.get_json.keys():
        return make_response('Missing name', 404)

    state.save()

    return make_response(jsonify(state.to_dict()), 201)


@app_views.route(
    '/states/<state_id>',
    methods=['PUT'],
    strict_slashes=False
)
def update_state(state_id):
    """
    Update a specified State object.

    Args:
        state_id : Id of the wantedState object.

    Returns:
        json: The updated State object with the status code 200.
    """
    state = storage.get(State, state_id)

    if not request.get_json:
        return make_response('Not a JSON', 400)

    if state is None:
        raise NotFound

    for key, stte in request.get_json().items():
        if key not in ('id', 'created_at', 'updated_at'):
            state.__setattr__(key, stte)

    state.save()

    return make_response(jsonify(state.to__dict()), 200)
