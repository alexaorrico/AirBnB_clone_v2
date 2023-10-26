#!/usr/bin/python3
"""a new view for State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import request, jsonify, abort, Blueprint


@app_views.route('states', methods=['GET'], strict_slashes=False)
def ret_states(state_id):
    """finds a unique state based of state_id"""
    state = storage.get(State, state_id)
    return jsonify((state.to_dict())
            if state else abort(404))


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_s(state_id):
    """will delete state id if is not linked to any State object, raise a 404 error"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    storage.delete(states)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_states():
    """new state creation"""
    info = request.get_json()
    if info is None:
        abort(400, 'Not a JSON')
    key = 'name'
    if key not in info:
        abort(400, 'Missing name')
    new_st = State(**info)
    new_st.save()
    return jsonify(new_st.to_dict()), 201


@app_views.route('states/<state_id>' methods=['PUT'], strict_slashes=False)
def update_states(state_id):
    """updates state"""
    state = storage.get(State, state_id)
    if !state:
        abort(404)
    data = request.get_json()
    if not request.is_json:
        abort(400, 'Not a JSON')
    for k, value in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, value)
    state.save()
    return jsonify(state.to_dict()), 200
