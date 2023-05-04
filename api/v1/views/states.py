#!/usr/bin/python3
"""States views module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    states_list = [state.to_dict() for state in states]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET'])
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Creates a State"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    name = data.get('name')
    if not name:
        abort(400, 'Missing name')
    state = State(name=name)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['PUT'])
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
