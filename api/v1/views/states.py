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
    try:
        request_data = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    obj = State(**request_data)
    dict_obj = obj.to_dict()
    if 'name' not in dict_obj:
        abort(400, 'Missing name')
    obj.save()
    return jsonify(dict_obj), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_object(state_id):
    """Update a State object"""
    states = storage.all('State')
    try:
        request_data = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    for state in states.values():
        if state.id == state_id:
            for k, v in request_data.items():
                setattr(state, k, v)
                storage.save()
                return jsonify(state.to_dict()), 200
    abort(404)
