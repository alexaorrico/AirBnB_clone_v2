#!/usr/bin/python3
"""
Route definitions for the 'states' view
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_state_list():
    """Returns list of stored State objects"""
    objs = list(storage.all(State).values())
    states = [obj.to_dict() for obj in objs]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Returns list of stored State objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a particular State object from the DB"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State object"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data.keys():
        abort(400, 'Missing name')
    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a particular stored State object"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    ignore = ['id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
