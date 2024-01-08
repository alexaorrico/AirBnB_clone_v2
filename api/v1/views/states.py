#!/usr/bin/python3

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models import *

@app_views.route('/states', methods=["GET"], strict_slashes=False)
def get_states():
    """get all state objects"""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """retrieve state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state():
    """method to delete state"""
    state = storage.get(Stae, state_id)
    if is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False
def create_state():
    """creates new state"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
     new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update state by id"""
    state =  storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
