#!/usr/bin/python3
""" Create a new view for states and handle RESTFul API"""
# api/v1/views/states.py

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Gets the list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<string:state_id>',
                 methods=['GET'], strict_slashes=False)
def get_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    if 'name' not in data:
        abort(400, description='Missing name')
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'])
def update_state(state_id):
    if request.is_json is False:
        abort(404, 'Not a JSON')
    data = request.get_json()
    states = storage.all(State)
    s_key = "State." + state_id
    if s_key not in states:
        abort(404)
    # Ignore keys: id, created_at, and updated_at
    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(states[s_key], key, value)
    storage.save()
    return jsonify(states[s_key].to_dict()), 200
