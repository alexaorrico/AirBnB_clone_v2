#!/usr/bin/python3
'''New view for State objects'''

from flask import Flask, abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_states():
    '''Getting all State objects'''
    objects = storage.all(State)
    lista = [state.to_dict() for state in objects.values()]
    return jsonify(lista)

@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    '''Retrieves a State object by its id'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    '''Creates a State'''
    response = request.get_json()
    if not response:
        abort(400, {'error': 'Not a JSON'})
    if "name" not in response:
        abort(400, {'error': 'Missing name'})
    state = State(**response)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''Updates a State object'''
    response = request.get_json()
    if not response:
        abort(400, {'error': 'Not a JSON'})
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in response.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())

@app_views.route('/states/<string:state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    '''Deletes a State object'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200
