#!/usr/bin/python3
"""
Contains the states view for the API.
"""

from models import storage
from api.v1.views import app_views
from models.state import State
from flask import jsonify, request, abort, make_response


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Define a route for
    retrieves the list of all State objects
    """
    state_obj = storage.all(State)
    # Convert each State object to a dictionary and return as JSON
    return jsonify([obj.to_dict() for obj in state_obj.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states_id(state_id):
    """
    Define a route for
    retrieves a State object by ID"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Define a route for
    deletes a State object by ID"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Define a route for creating a new State object
    """
    new_state = request.get_json()
    if not new_state:
        abort(400, 'Not a JSON')
    if 'name' not in new_state:
        abort(400, 'Missing name')
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Define a route for updating a specific State object by ID
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    # If the JSON data is missing or not valid JSON, return a 400 error
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
