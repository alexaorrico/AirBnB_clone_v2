#!/usr/bin/python3
""" A Flask route that returns json status response"""

from api.v1.views import app_views
from flask import current_app,jsonify, request, abort
from models import storage, state

State = state.State


@app_views.route('/states', methods=['GET'])
def get_states():
    """Returns all states object in json format"""
    states = [state.to_dict() for state in storage.all('State').values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Returns a specified state using the state id"""
    state = storage.get('State', state_id)
    if state is None:  # if id is not found return 404
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a specific state using the give id"""
    state = storage.get('State', state_id)
    # If the state_id is not linked to any State object, raise a 404 error
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a new state object"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201



@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a state object with the given id"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    try:
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
    except Exception as e:
        abort(400, f'Error parsing JSON: {str(e)}')



