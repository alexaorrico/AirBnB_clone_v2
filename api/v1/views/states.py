#!/usr/bin/python3
'''New view for State objects'''

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    '''Get all State objects'''
    objects = storage.all(State)
    return jsonify([state.to_dict() for state in objects.values()])


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id):
    '''Get a State object by ID'''
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    return jsonify(state_object.to_dict()), 200


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    '''Create a new State'''
    data = request.get_json()
    if not data:
        abort(400, {'error': 'Not a JSON'})
    if 'name' not in data:
        abort(400, {'error': 'Missing name'})
    state_object = State(**data)
    storage.new(state_object)
    storage.save()
    return jsonify(state_object.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    '''Update a State object'''
    data = request.get_json()
    if not data:
        abort(400, {'error': 'Not a JSON'})
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state_object, key, value)
    storage.save()
    return jsonify(state_object.to_dict()), 200


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    '''Delete a State object'''
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    storage.delete(state_object)
    storage.save()
    return jsonify({}), 200

