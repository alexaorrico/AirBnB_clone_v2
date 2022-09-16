#!/usr/bin/python3
"""Module with the view for State objects"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import request, abort, jsonify


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """Return a list of dictionaries of all states"""
    if request.method == 'GET':
        states = []
        for state in storage.all(State).values():
            states.append(state.to_dict())
        return jsonify(states)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    if 'name' not in data.keys():
        return 'Missing name', 400
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states_id(state_id):
    """Get a state instance from the storage"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        state.delete()
        storage.save()
        return {}, 200
    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return 'Not a JSON', 400
        for k, v in data.items():
            if k != 'id' or k != 'created_at' or k != 'updated_at':
                setattr(state, k, v)
        storage.save()
        return jsonify(state.to_dict()), 200
