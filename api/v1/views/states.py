#!/usr/bin/python3
"""
states module that handles all default RESTful API
actions.
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request, make_response


@app_views.route('/states',
                 methods=['GET'],
                 strict_slashes=False
                 )
def list_states():
    """List all `State` objects"""
    states_dict = storage.all(State)
    states_list = []
    for state in states_dict.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>',
                 methods=['GET'],
                 strict_slashes=False
                 )
def get_state(state_id):
    """Retrieves a `State` object."""
    state = storage.get(State, state_id)
    if state is not None:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False
                 )
def delete_state(state_id):
    """Deletes a `State` object."""
    state = storage.get(State, state_id)
    if state is not None:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states',
                 methods=['POST'],
                 strict_slashes=False
                 )
def create_state():
    """Creates a `State` object."""
    request_dict = request.get_json(silent=True)
    if request_dict is not None:
        if 'name' in request_dict.keys() and request_dict['name'] is not None:
            new_state = State(**request_dict)
            new_state.save()
            return make_response(jsonify(new_state.to_dict()), 201)
        return make_response(jsonify({'error': 'Missing name'}), 400)
    return make_response(jsonify({"error": "Not a JSON"}), 400)


@app_views.route('/states/<state_id>',
                 methods=['PUT'],
                 strict_slashes=False
                 )
def update_state(state_id):
    """Updates a `State` object."""
    request_dict = request.get_json(silent=True)
    if request_dict is not None:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        for key, val in request_dict.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, val)
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
    return make_response(jsonify({"error": "Not a JSON"}), 400)