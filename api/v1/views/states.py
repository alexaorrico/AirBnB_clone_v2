#!/usr/bin/python3
"""
States view module
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State)
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return make_response(jsonify(states_list))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return make_response(jsonify(state.to_dict()))


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state_by_id(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    request_dict = request.get_json(silent=True)
    if request.get_json() is not None:
        if 'name' in request_dict.keys() and request_dict['name'] is not None:
            new_state = State(**request_dict)
            new_state.save()
            return make_response(jsonify(new_state.to_dict()), 201)
        return make_response(jsonify({'error': 'Missing name'}), 400)
    return make_response(jsonify({'error': 'Not a JSON'}), 400)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ updates state object via PUT """
    request_dict = request.get_json(silent=True)
    if request_dict is not None:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        ignore_keys = ["id", "create_at", "update_at"]
        for key, value in request_dict.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
    return make_response(jsonify({'error': 'Not a JSON'}), 400)
