#!/usr/bin/python3
"""States view module"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_list():
    """Retrieves the list of all State objects"""
    states_list = []
    states_objs = storage.all('State').values()
    for element in states_objs:
        states_list.append(element.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_list_id(state_id):
    """Retrieves a specific State object by Id"""
    states_objs = storage.all('State').values()
    for element in states_objs:
        if element.id == state_id:
            return jsonify(element.to_dict())
    abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def states_remove(state_id):
    """Remove a state by Id"""
    state_to_delete = storage.get('State', state_id)
    if state_to_delete is None:
        abort(404)
    state_to_delete.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def new_state():
    """Creates a new state"""
    state_data = request.get_json()
    if state_data is None:
        abort(400, "Not a JSON")
    if not state_data.get('name'):
        abort(400, "Missing name")
    new_state = State(**state_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_update(state_id):
    """Updates one state based on its id"""
    data_for_update = request.get_json()
    if data_for_update is None:
        abort(400, "Not a JSON")
    forbiden_keys = ['id', 'created_at', 'updated_at']
    state_to_update = storage.get('State', state_id)
    if state_to_update is None:
        abort(404)
    for key, value in data_for_update.items():
        if key not in forbiden_keys:
            setattr(state_to_update, key, value)
    state_to_update.save()
    return jsonify(state_to_update.to_dict()), 200
