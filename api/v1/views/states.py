#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'])
def get_states():
    """ get all states """
    states = storage.all(State)
    states_list = []
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)

@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ get state """
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'error': 'Not found'}), 404
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'])
def create_state():
    """ create state """
    if not request.is_json:
        abort(400, 'Not a JSON')
    
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    
    state = State(**data)
    storage.new(state)
    storage.save()

    return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    state =storage.get(State, state_id)
    if state is None:
        abort(404)
    
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()

    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200