#!/usr/bin/python3
""" Show, Delete, Create and Update states """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_states(state_id=None):
    """ Endpoint that retrieves all states
        or retrieves one state by id

        state_id: id of the state to retrieve
    """
    all_states = storage.all('State')
    if not state_id:
        state_info = []
        for state in all_states.values():
            state_info.append(state.to_dict())
        return jsonify(state_info)
    else:
        state = "State.{}".format(state_id)
        if state in all_states:
            state = all_states[state]
            return jsonify(state.to_dict())
        else:
            abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """ Endpoint that deletes a specific state
        with the id

        state_id: id of the state to delete
    """
    all_states = storage.all('State')
    state = "State.{}".format(state_id)
    if state in all_states:
        state = all_states[state]
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False,
                 methods=['POST'])
def create_state():
    """ Endpoint that creates a state
        with the information given
    """
    info = request.get_json()
    if not info:
        abort(400, 'Not a JSON')
    if 'name' not in info:
        abort(400, 'Missing name')
    state = State(name=info['name'])
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['PUT'])
def modify_state(state_id):
    """ An endpoint that modifies a specific
    state with the id
    """
    info = request.get_json()
    if not info:
        abort(400, 'Not a JSON')
    all_states = storage.all('State')
    state_id = "State.{}".format(state_id)
    if state_id in all_states:
        state = all_states[state_id]
        for key, value in info.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(400)
