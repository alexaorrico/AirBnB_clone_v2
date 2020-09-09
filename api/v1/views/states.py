#!/usr/bin/python3
"""sturts"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, Blueprint, abort, request


@app_views.route('/api/v1/states', methods=['GET'], strict_slashes=False)
def get_states():
    """returns list of all states"""
    lizt = []
    states = storage.all(State).values()
    for state in states:
        lizt.append(state.to_dict())
    return jsonify(lizt)

@app_views.route('/api/v1/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_a_state():
    """finds a unique state based of state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    ret = state.to_dict()
    return jsonify(ret)
    


@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_a_state():
    """delete a specific state"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

@app_views.route('/api/v1/states', methods=['POST'], strict_slashes=False)
def create_a_state():
    """create a state"""
    req = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    key = 'name'
    if key not in req:
        abort(400, description="Missing name")
    new_state = State(**req)
    new_state.save()
    return jsonify(new_state), 201

@app_views.route('/api/v1/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_a_state():
    """ this method updates a state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    for key, value in state:
        if key is not "id" and key is not "created_at" and key is not "updated_at":
            state.update({'key':'value'})
    return jsonify(state), 200
