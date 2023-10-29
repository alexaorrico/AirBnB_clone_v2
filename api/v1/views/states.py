#!/usr/bin/python3
"""
This module hands the RESTFul API for states objects
"""

from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """
    Get state returns a state based on the state_id if found.
    If the state id 'state_id' is not given, it loads all the states
    And if a state ID 'state_id' is given, but cannot be mapped to any state
    a 404 error 'not found' is returned
    """
    if state_id is None:
        # request response for states without ID
        states = storage.all(State)
        state_response = []
        for state_id, state in states.items():
            state_response.append(state.to_dict())

        return jsonify(state_response)
    else:
        # request for states with ID
        state = storage.get(State, state_id)
        if state:
            return jsonify(state.to_dict())

        # raising 404 is ID is not a valid state_id
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    This function deletes a state given id 'state_id' exists for a state in
    the database. and 404 if it's not linked to a state
    """
    state = storage.get(State, state_id)
    # state doesn't exist, raise an error
    if state is None:
        abort(404)
    else:
        # deleting the state and return status code 200
        storage.delete(state)
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    This function creates a new state. Raises an error if the request
    is not in json format, and if the name attribute is missing, an error
    with the message 'Missing name' is returned.
    """

    try:
        data = request.get_json()
        # post request has no name attribute
        if 'name' not in data:
            return jsonify(error='Missing name'), 400

        # return the created state
        state = State(request.get_json())
        state = state.to_dict()
        return jsonify(state), 201

    # Not a valid json content type
    except BadRequest:
        return jsonify(error='Not a JSON'), 400


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    This function updates a state object in the database.
    If the ID is not linked to a state, a 404 error is raised
    if the content type is not JSON, a 404 error is raised
    in creating the state, ignore id, created_at and updated_at attributes
    """
    state = storage.get(State, state_id)
    # state doesn't exist, raise an error
    if state is None:
        abort(404)

    # request.get_jason returns none if parsing is not completed
    elif request.get_json() is None:
        return jsonify(error='Not a JSON'), 400

    # confirm if id, created_at or updated_at are in the contents
    for attribute, value in request.get_json():
        if attribute in ['id', 'created_at', 'updated_at']:
            pass
        else:
            state.__dict__[attribute] = value

    return jsonify(state.to_dict()), 200
