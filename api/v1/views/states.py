#!/usr/bin/python3
"""States for API"""

from models import storage
from models.state import State
from flask import request, jsonify, abort
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Gets all the states"""
    all_states = []
    for i in storage.all("State").values():
        all_states.append(i.to_dict())
    return jsonify(all_states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id):
    """Gets a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_states(state_id):
    """Deletes the states"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """Posts states"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    state_new = State(**data)
    storage.new(state_new)
    storage.save()
    return jsonify(state_new.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states(state_id):
    """Put States"""
    state = storage.get("State", state_id)
    if state_id is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key in ['id', 'created_at', 'updated_at']:
            pass
        else:
            new_info = {"name":state_id}
            data.update(new_info)
    storage.save()
    # = state.to_dict()
    return jsonify(data), 200
