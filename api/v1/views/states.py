#!/usr/bin/python3
"""
    Module of blueprints of flask
"""
from models import storage
from models.state import State
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def fetch_all_states():
    """Fetch all states"""
    states_list = []
    states = storage.all("State")
    for state in states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def fetch_state(state_id):
    """Fetch a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete a state"""
    state = storage.get("State", state_id)
    print(state)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a state"""
    post_data = request.get_json()
    if post_data is None:
        abort(400, 'Not a JSON')
    if post_data.get('name') is None:
        abort(400, 'Missing name')
    new_state = State(**post_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a state"""
    attributes_unchanged = ['id', 'created_at', 'updated_at']
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    put_data = request.get_json()
    if put_data is None:
        abort(400, 'Not a JSON')
    for key, value in put_data.items():
        if key in attributes_unchanged:
            pass
        else:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
