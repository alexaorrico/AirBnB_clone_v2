#!/usr/bin/python3
"""
all restful api actions that is taken by
this view state
"""

from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_all():
    """all state objects to be returned by this list"""
    states_all = []
    states = storage.all("State").values()
    for state in states:
        states_all.append(state.to_json())
    return jsonify(states_all)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_get(state_id):
    """ GET method to be handled"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state = state.to_json()
    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def state_delete(state_id):
    """delete method to be handled"""
    empty_dict = {}
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """post method to be handled"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    state = State(**data)
    state.save()
    state = state.to_json()
    return jsonify(state), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_put(state_id):
    """ put method to be handled"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            state.bm_update(key, value)
    state.save()
    state = state.to_json()
    return jsonify(state), 200
