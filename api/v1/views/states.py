#!/usr/bin/python3
'''BLueprint implementation for state model'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('states/<state_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def handle_states(state_id=None):
    '''Return the list of all State objects'''
    if request.method == 'DELETE':
        return del_state(state_id)
    elif request.method == 'POST':
        return add_state()
    elif request.method == 'PUT':
        return update_state(state_id)
    elif request.method == 'GET':
        return get_states(state_id)


def get_states(state_id=None):
    '''Handles all get request to states endpoint'''
    if state_id:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        return jsonify(state.to_dict())
    states_k = [val.to_dict() for val in storage.all(State).values()]
    return jsonify(states_k)


def del_state(state_id):
    '''Deletes a state obj with state_id'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


def add_state():
    '''Adds state to states'''
    try:
        req_data = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if type(req_data) is not dict:
        abort(400, 'Not a JSON')
    if 'name' not in req_data:
        abort(400, 'Missing name')
    state = State(**req_data)
    state.save()
    return get_states(state.id), 201


def update_state(state_id):
    '''Update a state instance'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        req_data = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if type(req_data) is not dict:
        abort(400, 'Not a JSON')
    for key, val in req_data.items():
        if key != 'id' or key != 'created_at' or key != 'updated_at':
            setattr(state, key, val)
    state.save()
    return get_states(state.id), 200
