#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API actions
"""

import json
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def retrieve_states():
    """
    REtrieve states
    """
    states_list = []
    states = storage.all(State).values()
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def retrieve_state(state_id):
    """
    Retrieves states using the state id
    Raises a 404 error if the id isnt found
    """
    state = storage.get(State, state_id)
    if state:
        return make_response(jsonify(state.to_dict()), 200)
    else:
        abort(400)


@app_views.route("/states/<string:state_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a state using the state id
    Raises a 404 error if the id isnt found
    """
    state = storage.get(State, str(state_id))
    if state:
        state.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route("/states/", methods=["POST"], strict_slashes=False)
def post_state():
    """
    Posts a new state
    """
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>",
                 methods=["PUT"], strict_slashes=False)
def put_state(state_id):
    """
    Updates a state using the state id
    Raises a 404 error if the id doesnt match any state
    """
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(400, "Not a JSON")
        update = request.get_json()
        keys_ignore = ["id", "created_at", "updated_at"]
        for key, value in update.items():
            if key not in keys_ignore:
                setattr(state, key, value)
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
    else:
        abort(404)
