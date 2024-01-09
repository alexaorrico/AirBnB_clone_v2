#!/usr/bin/python3
"""Module for handling states in the API"""

# Import statements
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Get state information for all states"""
    states_list = []
    for state_instance in storage.all("State").values():
        states_list.append(state_instance.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Get state information for the specified state"""
    specified_state = storage.get("State", state_id)
    if specified_state is None:
        abort(404)
    return jsonify(specified_state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state based on its state_id"""
    specified_state = storage.get("State", state_id)
    if specified_state is None:
        abort(404)
    specified_state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """Create a new state"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_state = State(**request.get_json())
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """Update a state"""
    specified_state = storage.get("State", state_id)
    if specified_state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(specified_state, attr, val)
    specified_state.save()
    return jsonify(specified_state.to_dict())
