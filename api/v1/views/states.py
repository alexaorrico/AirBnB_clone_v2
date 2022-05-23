#!/usr/bin/python3
""" view for State objects that handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """ Retrieves the list of all State objects and create a new State"""

    # retrieves State object
    if request.method == 'GET':
        states = storage.all(State)
        states_list = []
        for key, value in states.items():
            states_list.append(value.to_dict())
        return jsonify(states_list)

    # create a State
    elif request.method == 'POST':
        # transform the HTTP body request to a dictionary
        body_request_dict = request.get_json()

        # If the HTTP body request is not valid JSON
        if not body_request_dict:
            abort(400, 'Not a JSON')

        # If the dictionary doesn’t contain the key name
        if 'name' not in body_request_dict:
            abort(400, 'Missing name')

        # create new object State with body_request_dict
        new_state = State(**body_request_dict)

        storage.new(new_state)
        storage.save()
        return new_state.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def state_id(state_id):
    """
        Retrieves a State object
    """
    state_catch = storage.get(State, state_id)

    # If the state_id is not linked to any State object, raise a 404 error
    if state_catch is None:
        abort(404)

    # Retrieves a State object
    if request.method == 'GET':
        return state_catch.to_dict()

    # Deletes a State object
    if request.method == 'DELETE':
        empty_dict = {}
        storage.delete(state_catch)
        storage.save()
        return empty_dict, 200

    # update a State object
    if request.method == 'PUT':
        # transform the HTTP body request to a dictionary
        body_request_dict = request.get_json()

        # If the HTTP body request is not valid JSON
        if not body_request_dict:
            abort(400, 'Not a JSON')

        # Update the State object with all key-value pairs of the dictionary
        # Ignore keys: id, created_at and updated_at

        for key, value in body_request_dict.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state_catch, key, value)

        state_catch.save()
        return state_catch.to_dict(), 200
