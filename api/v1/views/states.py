#!/usr/bin/python3
"""
Module for view for State objects
It handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states_list():
    """Retrieves the list of all State objects"""
    states_list = []
    states = storage.all(State).values()
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list), 200


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states_obj(state_id):
    """
    Retrieves a State object

    Args:
        state_id: The id of the state object
    Raises:
        404: if state_id supplied is not linked to any state object
    """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict()), 200
    else:
        return jsonify({"error": "Not found"}), 404


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_states_obj(state_id):
    """
    Deletes a State object

    Args:
        state_id: The id of the state object
    Raises:
        404: if state_id supplied is not linked to any state object
    """
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """
    Creates a State object

    Returns:
        The new State with the status code 201
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a state object

    Args:
        state_id: The id of the state object
    Raises:
        404:
            If state_id supplied is not linked to any state o    bject
            400: If the HTTP body request is not valid JSON
    """
    state = storage.get(State, state_id)
    if not state:
        return jsonify({'error': 'Not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    data.pop('id', None)
    data.pop('created_at', None)
    data.pop('updated_at', None)
    for key, value in data.items():
        setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
