#!/usr/bin/python3
"""
State view module
"""
from models import storage
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_all_state():
    """retrieve list of all State objects"""
    state_dict = storage.all("State")
    return jsonify([state.to_dict() for state in state_dict.values()])


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_a_state(state_id):
    """retrieve a state object according to state id"""
    state = storage.get("State", state_id)
    if state is not None:
        return state.to_dict()
    else:
        abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """delete State object at state_id and returns 200 otherwise 404"""
    state = storage.get("State", state_id)
    if state is not None:
        storage.delete(state)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state():
    """create state via POST"""
    json_data = request.get_json()
    if json_data is None:
        return "Not a JSON", 400
    elif "name" not in json_data:
        return "Missing name", 400
    else:
        new_state = State(**json_data)
        new_state.save()
        return new_state.to_dict(), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """update State object"""
    ignore = ["id", "created_at", "updated_at"]
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    json_data = request.get_json()
    if json_data is not None:
        for key, value in json_data.items():
            if key not in ignore:
                setattr(state, key, value)
        storage.save()
        return state.to_dict(), 200
    else:
        return "Not a JSON", 400
