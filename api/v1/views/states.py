#!/usr/bin/python3
'''
methods and routes for working with state data
'''
from models.state import State
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    '''
    Gets all of the states listed
    '''
    all_states = []
    for i in storage.all("State").values():
        all_states.append(i.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_by_id(state_id):
    '''
    gets the state by state id
    '''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    '''
    deletes a state if given the id
    '''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return ({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    '''
    adds a state to the DB
    '''
    state = request.get_json()
    if state is None:
        abort(400, 'not a JSON')
    if 'name' not in state:
        abort(400, 'Missing Name')
    new_state = State(**state)
    storage.new(new_state)
    storage.save()
    return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''
    updates a state in the DB
    '''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_info = request.get_json()
    if state_info is None:
        abort(400, 'not a JSON')
    for key, value in state_info.items():
        if key in ['id', 'created_at', 'updated_at']:
            pass
        else:
            setattr(state, key, value)
    storage.save()
    all_states = state.to_dict()
    return(jsonify(all_states), 200)
