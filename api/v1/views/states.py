#!/usr/bin/python3
"""This handles views for states"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, request, abort
import json


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """This returns all states"""
    states = storage.all(State).values()
    states_list = [state.to_dict() for state in states]
    return json.dumps(states_list, indent=2)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """Returns the state with that id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return json.dumps(state.to_dict(), indent=2)


@app_views.route(
        '/states/<state_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_state(state_id):
    """This deletes a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return json.dumps({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """This function creates a state"""
    state_to_create = request.get_json()
    if not state_to_create:
        abort(400, "Not a JSON")
    if "name" not in state_to_create:
        abort(400, "Missing name")
    new_state = State(**state_to_create)
    new_state.save()
    return json.dumps(new_state.to_dict(), indent=2), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update the state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data_to_put = request.get_json()
    if not data_to_put:
        abort(400, "Not a JSON")
    for key, value in data_to_put.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return json.dumps(state.to_dict(), indent=2), 200
