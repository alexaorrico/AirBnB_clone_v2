#!/usr/bin/python3
"""
Contains the states view for the AirBnB clone v3 API.
Handles all default RESTful API actions for State objects.
"""
from flask import jsonify, request, abort
from werkzeug.exceptions import NotFound, BadRequest

from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects.
    """
    all_states = storage.all(State).values()
    states_list = [state.to_dict() for state in all_states]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object by its id.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a State object from the JSON body request.
    """
    request_data = request.get_json()
    if not request_data:
        raise BadRequest(description='Not a JSON')
    if 'name' not in request_data:
        raise BadRequest(description='Missing name')
    new_state = State(**request_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object by its id.
    """
    state_to_delete = storage.get(State, state_id)
    if not state_to_delete:
        abort(404)
    storage.delete(state_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object by its id with the information
    from the JSON body request.
    """
    state_to_update = storage.get(State, state_id)
    if not state_to_update:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        raise BadRequest(description='Not a JSON')
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in request_data.items():
        if key not in ignore_keys:
            setattr(state_to_update, key, value)
    state_to_update.save()
    return jsonify(state_to_update.to_dict()), 200
