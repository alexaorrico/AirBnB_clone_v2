#!/usr/bin/python3
"""
    This module creates a new view for State
    objects that handles all default REST API
    actions.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves all states in storage"""
    all_states = storage.all(State).values()
    states_list = []
    for state in all_states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=['GET'],
                 strict_slashes=False)
def get_specific_state(state_id):
    """Return the state with given id"""
    search_result = storage.get(State, state_id)
    if search_result:
        return jsonify(search_result.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_specific_state(state_id):
    """Delete the state with given id"""
    search_result = storage.get(State, state_id)
    if search_result:
        storage.delete(search_result)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/states/", methods=['POST'],
                 strict_slashes=False)
def post_new_state():
    """Post a new state to the db"""
    try:
        state_dict = request.get_json()

    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    if state_dict.get("name"):
        new_state = State(**state_dict)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201

    return jsonify({"error": "Missing name"}), 400


@app_views.route("/states/<state_id>", methods=['PUT'],
                 strict_slashes=False)
def modify_state(state_id):
    """Modify an existing state in the db"""
    state = storage.get(State, state_id)
    if state:
        try:
            update_dict = request.get_json()
            for key in ('id', 'created_at', 'updated_at'):
                if update_dict.get(key):
                    del update_dict[key]

        except Exception:
            return jsonify({"error": "Not a JSON"}), 400

        for key, value in update_dict.items():
            setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200

    else:
        abort(404)
