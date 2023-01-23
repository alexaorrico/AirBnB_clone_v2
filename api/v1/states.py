#!/usr/bin/python3
'''Contains the states view for the API.'''
from flask import jsonify, request, abort
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    '''Get all states'''
    query = storage.all(State).values()
    states = list(map(lambda x: x.to_dict(), query))
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    '''Gets the state base on id'''
    query = storage.all(State).values()
    if state_id:
        state = list(filter(lambda x: x.id == state_id, query))
        if state:
            return jsonify(state[0].to_dict())
        raise NotFound()


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    '''delete a state with the given id.'''
    states = storage.all(State).values()
    query = list(filter(lambda x: x.id == state_id, states))
    if query:
        storage.delete(query[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state(state_id=None):
    '''creat a new state.'''
    req = request.get_json()
    if type(req) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in req:
        raise BadRequest(description='Missing name')
    new_state = State(**req)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    '''Updates the state base on an id.'''
    ignore = ('id', 'created_at', 'updated_at')
    query = storage.all(State).values()
    result = list(filter(lambda x: x.id == state_id, query))
    if result:
        req = request.get_json()
        if type(req) is not dict:
            raise BadRequest(description='Not a JSON')
        states = result[0]
        for key, value in req.items():
            if key not in ignore:
                setattr(states, key, value)
        states.save()
        return jsonify(states.to_dict()), 200
    raise NotFound()
