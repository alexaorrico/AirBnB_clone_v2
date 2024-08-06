#!/usr/bin/python3
"""This is module states"""

from api.v1.views import (app_views, State, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def view_all_states():
    """Example endpoint returning a list of all the states"""
    all_states = [state.to_json() for state in storage.all("State").values()]
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def view_one_state(state_id=None):
    """Example endpoint returning a list of one state"""
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_json())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """Example endpoint deleting one state"""
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Example endpoint creating a state"""
    r = None
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    if 'name' not in r.keys():
        return "Missing name", 400
    s = State(**r)
    s.save()
    return jsonify(s.to_json()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """Example endpoint updates a state"""
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    for k in ("id", "created_at", "updated_at"):
        r.pop(k, None)
    for k, v in r.items():
        setattr(state, k, v)
    state.save()
    return jsonify(state.to_json()), 200
