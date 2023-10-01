#!/usr/bin/python3
"""
This module defines a Flask web application that
provides a RESTful API for State objects.
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel, Base
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects.
    """
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states), 200


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object by its ID.
    """
    state = next((state for state in storage.all(State).values()
                 if state.id == state_id), None)
    if state is None:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes a State object by its ID.
    """
    state = next((state for state in storage.all(State).values()
                 if state.id == state_id), None)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object by its ID.
    """
    state = next((state for state in storage.all(State).values()
                 if state.id == state_id), None)
    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a new State object.
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    state = State(name=data['name'])
    state.save()
    return jsonify(state.to_dict()), 201
