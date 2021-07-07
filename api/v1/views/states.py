#!/usr/bin/python3
"""Module to create a new view for State objects"""
from flask import jsonify, Flask, request, abort
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    all_states = storage.all('State')
    my_list = []
    for value in all_states.values():
        my_list.append(value.to_dict())
    return (jsonify(my_list))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """Retrieves the state by ID"""
    state = storage.get('State', str(state_id))
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """Deletes a state by ID"""
    state = storage.get('State', str(state_id))
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Post a State object"""
    data = request.get_json(silent=True)
    if not data:
        abort(400)
        abort(Response("Not a JSON"))
    if 'name' not in data:
        abort(400)
        abort(Response("Missing name"))
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Put a State object"""
    state = storage.get('State', str(state_id))
    if state is None:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400)
        abort(Response("Not a JSON"))

    # TODO
    # Ignore id, created_at and updated_at
    for k, v in data.items():
        setattr(state, k, v)

    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 200
