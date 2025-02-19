#!/usr/bin/python3
""" API """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    '''Gets the list of all states.'''
    all_states = storage.all(State).values()
    state_list = list(map(lambda x: x.to_dict(), all_states))
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    '''Gets the state with the given id.'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    '''Deletes a state with the given id.'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    '''Creates a new state.'''
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, description='Not a JSON')
    if 'name' not in data:
        abort(400, description='Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def modify_state(state_id):
    '''Updates the state with the given id.'''
    exclude_keys = ('id', 'created_at', 'updated_at')
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in exclude_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
