#!/usr/bin/python3
''' new view for State objects'''

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    '''Get a list of all State objects'''
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    '''Get a State object by ID'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''Create a new State object'''
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''Update a State object'''
    state = storage.get(
        State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    '''Delete a State object by ID'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200
