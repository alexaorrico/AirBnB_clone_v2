#!/usr/bin/python3
"""Module with a flask script"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

@app_views.route('/states/', methods=["GET"])
def states():
    """Get all state objects"""
    array_of_states = []

    all_states = storage.all(State)

    for state in all_states.values():
        dict_state = state.to_dict()
        array_of_states.append(dict_state)

    return jsonify(array_of_states)


@app_views.route("/states/<state_id>", methods=["GET"])
def state_get(state_id):
    """Get a state object"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def state_delete(state_id):
    """Delete a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def state_create():
    """Create a new State"""
    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    if 'name' not in data:
        abort(400, "Missing name")

    new_state = State(**data)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_update(state_id):
    """Update a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    state.save()

    return jsonify(state.to_dict()), 200
