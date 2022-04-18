#!/usr/bin/python3
"""State view model"""
from flask import abort
from flask import jsonify
from flask import request
from models import storage
from models.state import State
from api.v1.views import app_views

# states_objs = storage.all('State')


def get_states():
    """Returns a list of all state models."""
    states_objs = storage.all('State')
    states = [obj.to_dict() for obj in states_objs.values()]

    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """Returns a specified state model."""
    states_objs = storage.all('State')
    state_id = "State." + state_id

    if state_id not in states_objs.keys():
        abort(404)

    state = states_objs.get(state_id)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Deletes a specified state model."""
    states_objs = storage.all('State')
    state_id = "State." + state_id

    if state_id not in states_objs.keys():
        abort(404)

    storage.all().pop(state_id)
    storage.save()

    return jsonify({}), 200, {'ContentType': 'application/json'}


@app_views.route('/states/', strict_slashes=False, methods=['POST'])
def create_state():
    """Creates a new state object."""
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.get_json().keys():
        abort(400, 'Missing name')

    state = (State(**request.get_json()))
    storage.new(state)
    return state.to_dict(), 201, {'ContentType': 'application/json'}


@app_views.route('/states/<state_id>', strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    """Modifies a state object."""
    states_objs = storage.all('State')
    state_id = "State." + state_id

    if not request.json:
        abort(400, "Not a JSON")
    if state_id not in states_objs.keys():
        abort(404)

    state = State(**request.get_json())
    state.save()

    return state.to_dict(), 200, {'ContentType': 'application/json'}
