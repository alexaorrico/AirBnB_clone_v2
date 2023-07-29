#!/usr/bin/python3
"""
This module handles the view for State objects that handles
all default RESTFul API actions
"""

from flask import jsonify, abort, request
from api.v1.views import state_views
from models import storage
from models.state import State


@state_views.route("/", methods=["GET"])
def list_states():
    """Retrieves the list of all State objects"""
    states_objs = storage.all(State)
    states_list = []
    for state in states_objs.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@state_views.route("/<state_id>", methods=["GET"])
def get_state(state_id):
    """Retrieves a State object by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@state_views.route("/<string:state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Deletes a State object by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@state_views.route("/", methods=["POST"])
def create_state():
    """Creates a new State and stores it"""
    state_data = request.get_json()
    if not state_data:
        abort(400, "Not a JSON")
    if 'name' not in state_data:
        abort(400, "Missing name")
    state = State(**state_data)
    state.save()
    return jsonify(state.to_dict()), 201


@state_views.route("/<string:state_id>", methods=["PUT"])
def update_state(state_id):
    """Updates a State given by state_id and stores it"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    if len(request.data) == 0:
        abort(400, "Not a JSON")
    state_data = request.get_json()
    if not state_data:
        abort(400, "Not a JSON")
    for key, value in state_data.items():
        keys_to_ignore = ["id", "created_at", "updated_at"]
        if key not in keys_to_ignore:
            setattr(state, key, value)
    state.save()
    storage.save()
    state = state.to_dict()
    return jsonify(state), 200
