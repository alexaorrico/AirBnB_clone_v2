#!/usr/bin/python3

'''
This module contains the State class
Routes:
    /states - Returns a list of the states
    GET /states/<id> - Returns a state object
    DELETE /states/<id> - Deletes a state object
    POST /states - Creates a state object
    PUT /states/<id> - Updates a state object
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    '''
    Retrieves the list of all State objects
    '''
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id=None):
    '''
    Retrieves a State object
    '''
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    '''
    Deletes a State object
    '''
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def make_state():
    '''
    Creates a State object
    '''
    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    if 'name' not in body:
        abort(400, 'Missing name')
    state = State(**body)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id=None):
    '''
    Updates a State object
    '''
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')
    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    for k, v in body.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict()), 200
