#!/usr/bin/python3
"""Handles the states view
"""

# from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Gets the dict containing all the states
    """
    states = storage.all("State")
    list_states = []
    for state in states.values():
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """Gets a state by its ID
    """
    state = storage.get("State", state_id)
    if state is not None:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_states(state_id):
    """Deletes a state
    """
    state = storage.get("State", state_id)
    if state is not None:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a state
    """
    got_json = request.get_json()
    if not got_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in got_json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_state = State(**got_json)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Updates a state
    """
    got_json = request.get_json()
    if not got_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    state = storage.get("State", state_id)
    if state:
        for key, val in got_json.items():
            setattr(state, key, value)
        storage.save()
        return make_response(jsonify(state.to_dict), 200)
    else:
        abort(404)
