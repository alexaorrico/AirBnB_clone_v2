#!/usr/bin/python3
"""
State API
"""

from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states/', methods=["GET"])
@app_views.route('/states', methods=["GET"])
def all_states():
    """GET ALL states"""
    all_li = []
    for value in storage.all(State).values():
        all_li.append(value.to_dict())
    return (jsonify(all_li))


@app_views.route('/states/<string:id>', methods=["GET"])
def state(id):
    """GET State by id"""
    state_id = storage.get(State, id)
    if state_id is None:
        abort(404)
    return (jsonify(state_id.to_dict()))


@app_views.route('/states/<string:id>', methods=["DELETE"])
def remove_state(id):
    """Remove State by id"""
    state_id = storage.get(State, id)
    if state_id is None:
        abort(404)
    storage.delete(state_id)
    storage.save()
    return {}, 200


@app_views.route('/states/', methods=["POST"])
def create_state(strict_slashes=False):
    """CREATE State"""
    if request.is_json:
        json_state = request.get_json()
        if json_state.get("name") is None:
            abort(400, description="Missing name")
        else:
            new = State(**json_state)
            storage.new(new)
            storage.save()
            return new.to_dict(), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/states/<string:id>', methods=["PUT"])
def update_state(id):
    """UPDATE State by id"""
    state = storage.get(State, id)
    if state is None:
        abort(404)
    if request.is_json:
        forbidden = ["id", "created_at", "updated_at"]
        json_state = request.get_json()
        storage.delete(state)
        for k, v in json_state.items():
            if json_state[k] not in forbidden:
                setattr(state, k, v)
        storage.new(state)
        storage.save()
        return state.to_dict(), 200
    else:
        abort(400, description="Not a JSON")
