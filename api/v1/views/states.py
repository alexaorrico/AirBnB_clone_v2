#!/usr/bin/python3
"""States view"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """retrieve all states"""
    states = storage.all(State)
    lists = []
    for state in states.values():
        lists.append(state.to_dict())
    return jsonify(lists)


@app_views.route('/states/<state_id>/', methods=['GET'],
                 strict_slashes=False)
def get_state_id(state_id):
    """get state by id"""
    objects = storage.get(State, state_id)
    if objects is None:
        abort(404)
    return jsonify(objects.to_dict()), '200'


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """Update a State object"""
    response = request.get_json()
    if response is None:
        abort(400, {'Not a JSON'})
    if "name" not in response:
        abort(400, {'Missing name'})
    stateObject = State(name=response['name'])
    storage.new(stateObject)
    storage.save()
    return jsonify(stateObject.to_dict()), '201'


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Update a State object"""
    response = request.get_json()
    if response is None:
        abort(400, {'Not a JSON'})
    stateObject = storage.get(State, state_id)
    if stateObject is None:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in response.items():
        if key not in ignore_keys:
            setattr(stateObject, key, value)
    storage.save()
    return jsonify(stateObject.to_dict()), '200'


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    stateObject = storage.get(State, state_id)
    if stateObject is None:
        abort(404)
    storage.delete(stateObject)
    storage.save()
    return jsonify({}), '200'
