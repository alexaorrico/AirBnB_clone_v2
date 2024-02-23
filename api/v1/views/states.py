#!/usr/bin/python3
"""
Handles default State object RESTful API actions

"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """This route fetches all State objects"""
    states = []
    for state in storage.all(State).values():
        state_dict = state.to_dict()
        states.append(state_dict)
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Fetches a State object"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a State object"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    ignore = ["id", "created_at", "updated_at"]
    for key, value in request.get_json().items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
