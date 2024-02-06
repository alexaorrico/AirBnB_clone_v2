#!/usr/bin/python3
'''New view for State objects'''

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import State
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    '''Get status'''
    objects = storage.all(State)
    lista = [state.to_dict() for state in objects.values()]
    return jsonify(lista)

@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    '''Get a State object by ID'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    '''Create a State'''
    data = request.get_json()
    if data is None:
        abort(400, {'error': 'Not a JSON'})
    if "name" not in data:
        abort(400, {'error': 'Missing name'})
    state = State(**data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''Update a State object'''
    data = request.get_json()
    if data is None:
        abort(400, {'error': 'Not a JSON'})
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    '''Delete a State object'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200
