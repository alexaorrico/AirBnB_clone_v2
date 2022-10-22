#!/usr/bin/python3
"""State route"""
import json


from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage

@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """retrieves state [by id | all<default>]"""
    if state_id is None:
        list_all = []
        all_state = storage.all(State)
        for state in all_state.values():
            list_all.append(state.to_dict())
        return jsonify(list_all), 200
    else:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """deletes an instance of state from storage"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    return jsonify({}), 200


@app_views.route('/states', methods=['POST', 'PUT'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['POST', 'PUT'],
                 strict_slashes=False)
def post_state(state_id=None):
    """creates a new instance of state"""
    req = request.get_json()
    if req is None:
        abort(400, message="Not a JSON")

    if request.method == "POST":
        if 'name' not in req.keys():
            abort(400, message="Missing name")
        else:
            state = State(req)
            return jsonify(state.to_dict()), 201
    elif request.method == "PUT":
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        for i, j in req.items():
            if i not in ["id", "created_at", "updated_at"]:
                setattr(state, i, j)
        storage.save()
        return jsonify(state.to_dict()), 200
