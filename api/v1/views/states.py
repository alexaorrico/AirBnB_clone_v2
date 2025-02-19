#!/usr/bin/python3
"""state.py"""

from flask import jsonify
from flask import abort
from flask import request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states")
def get_states():
    """retrieves all states """
    states = []
    states_obj = storage.all(State)
    for state_obj in states_obj.values():
        states.append(state_obj.to_dict())

    return jsonify(states), 200


@app_views.route("/states/<string:state_id>")
def get_state(state_id=None):
    """retrieves a specific state """
    if state_id is None:
        abort(404)

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<string:state_id>", methods=['DELETE'])
def delete_state(state_id=None):
    """retrieves a specific state """
    if state_id is None:
        abort(404)

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return {}, 200


@app_views.route("/states/", methods=['POST'])
def create_state():
    """ Creates a state"""
    state_dict = None
    try:
        state_dict = request.get_json()
    except Exception:
        if not isinstance(state_dict, dict):
            return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in state_dict:
        return jsonify({"error": "Missing name"}), 400
    state = State(name=state_dict['name'])
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'])
def update_state(state_id=None):
    """ updates a state object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_dict = None
    try:
        state_dict = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    for key, val in state_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, val)

    storage.save()
    return jsonify(state.to_dict()), 200
