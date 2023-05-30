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
        state_list.append(state.to_dict())
    return jsonify(states_list)

@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ get state """
    state.storage.get(State, state_id)
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
        return jsonify({'error': 'Not found'}), 404

    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': 'Not found'}), 404

    state = State(**data)
