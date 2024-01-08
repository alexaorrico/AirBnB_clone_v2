#!/usr/bin/python3
"""this module handles all default RESTFul API actions"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views

import models
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    all_states = models.storage.all(State)
    man = [x.to_dict() for x in all_states.values()]
    return jsonify(man)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    state = models.storage.get(State, state_id)
    if state is not None:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    state = models.storage.get(State, state_id)
    if state is not None:
        models.storage.delete(state)
        models.storage.save()
        return {}, 200
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """
    Creates a State
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = State(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """
    updates a state give a valid id
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    state = models.storage.get(State, state_id)
    if state is None:
        abort(400)

    ignore = ['id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    models.storage.save()
    return make_response(jsonify(state.to_dict()), 200)
