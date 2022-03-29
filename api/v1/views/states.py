#!/usr/bin/python3
""" API view for State objects. """
from api.v1.views import app_views
from flask import jsonify, request, abort
import json
from models import storage
from models.state import State
import os


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_states(text="is-cool"):
    """ Returns list of all State objs. """
    all_states = list(storage.all(State).values())
    list_all_states = []
    for state in all_states:
        list_all_states.append(state.to_dict())
    return jsonify(list_all_states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """ Returns the State obj in JSON. """
    try:
        state = storage.all(State)["State.{}".format(state_id)]
    except (TypeError, KeyError):
        abort(404)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes the State obj from storage. """
    try:
        state = storage.all(State)["State.{}".format(state_id)]
    except (TypeError, KeyError):
        abort(404)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state(text="is_cool"):
    """ Creates a new State obj. """
    content = request.get_json()
    try:
        json.dumps(content)
        if 'name' not in content:
            abort(400, {'message': 'Missing name'})
    except (TypeError, OverflowError):
        abort(400, {'message': 'Not a JSON'})
    new_state = State(**content)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def state_update(state_id):
    """Updates a state"""
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        state_dict = request.get_json()
        state = storage.get(State, state_id)
        if state is None:
            return abort(404)
        for key, value in state_dict.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict())
