#!/usr/bin/python3
"""module for the state file"""


from models import storage
from models.state import State
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/states", methods=['Get'], strict_slashes=False)
def retrieving_states():
    """retrieving the list of the states"""
    state_list = []
    states = storage.all("State")
    for state in states.values():
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def retrieve_state(state_id):
    """retrieving the state id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def deleting_state(state_id):
    """deleting a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", mehtods=['POST'], strict_slashes=False)
def creating_state():
    """creating a state"""
    post_data = request.get_json()
    if post_data is None:
        abort(400, "Not a JSON")
    if post_data.get("name") is None:
        abort(400, "Missing name")
    new_state = State(**post_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updating the state"""
    keys_ignored = ['id', 'created_at', 'updated_at']
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    put_data = request.get_json()
    if put_data is None:
        abort(404, "Not a JSON")
    for key, value in put_data.items():
        if key in keys_ignored:
            pass
        else:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
