#!/usr/bin/python3
"""view for State objects"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def all_states():
    """Retrieves the list of all State"""
    states = storage.all('State')
    new_list = []
    for state in states.values():
        new_list.append(state.to_dict())
    return jsonify(new_list)


@app_views.route('/states/<state_id>', strict_slashes=False)
def all_states_by_id(state_id):
    """Retrieves a state by a given ID"""
    states = storage.all('State')
    for state in states.values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route(
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def delete_object(state_id):
    """Deletes a State object"""
    states = storage.all('State')
    for state in states.values():
        if state.id == state_id:
            state.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_object():
    """Creates a State object"""
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request_data:
        return jsonify({"error": "Missing name"}), 400
    obj = State(**request_data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_object(state_id):
    """Update a State object"""
    states = storage.all('State')
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400
    for state in states.values():
        if state.id == state_id:
            for k, v in request_data.items():
                setattr(state, k, v)
            storage.save()
            return jsonify(state.to_dict()), 200
    abort(404)
