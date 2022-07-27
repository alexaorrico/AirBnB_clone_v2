#!/usr/bin/python3
"""State view model"""
import json
from flask import abort, make_response
from flask import jsonify
from flask import request
from models import storage
from models.state import State
from api.v1.views import app_views


# states_objs = storage.all('State')
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves a list of all state objects."""
    states_objs = storage.all('State')
    states = [obj.to_dict() for obj in states_objs.values()]

    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Returns a specified state model."""
    states_objs = storage.all('State')
    state_id = "State." + state_id

    if state_id not in states_objs.keys():
        abort(404)

    state = states_objs.get(state_id)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Deletes a specified state model."""
    states_objs = storage.all('State')
    state_id = "State." + state_id

    if state_id not in states_objs.keys():
        abort(404)

    storage.all().pop(state_id)
    storage.save()

    return jsonify({}), 200, {'ContentType': 'application/json'}


@app_views.route('/states/', strict_slashes=False, methods=['POST'])
def create_state():
    """Creates a new state object."""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "name" not in request.get_json().keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)

    state = State(**request.get_json())
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)

@app_views.route('/states/<state_id>', strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    """Modifies a state object."""
    states_objs = storage.all('State')
    state_id = "State." + state_id

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if state_id not in states_objs.keys():
        abort(404)

    state = states_objs.get(state_id)    
    ignored_keys = ['id', 'created_at', 'updated_at']
    for k, v in request.get_json().items():
        if k not in ignored_keys:
            setattr(state, k, v)

    state.save()
    return jsonify(state.to_dict())