#!/usr/bin/python3
"""sturts"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, Blueprint, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """returns list of all states"""
    lizt = []
    states = storage.all(State).values()
    for state in states:
        lizt.append(state.to_dict())
    return jsonify(lizt)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_a_state(state_id):
    """finds a unique state based of state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    ret = state.to_dict()
    return jsonify(ret)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_state(state_id):
    """delete a specific state"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    storage.delete(states)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_a_state():
    """create a state"""
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    key = 'name'
    if key not in req:
        abort(400, "Missing name")
    new_state = State(**req)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_a_state(state_id):
    """ this method updates a state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    for k, value in req.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, value)
    storage.save()
    return jsonify(state.to_dict()), 200
