#!/usr/bin/python3
""" New view for states """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


# Route to get all states
@app_views.route("/states", methods=['GET'], strict_slashes=False)
def states():
    states = storage.all(State)
    list_states = []
    for state in states.values():
        list_states.append(state.to_dict())
    return jsonify(list_states)


# Route to get a single state by ID
@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


# Route to delete a single state by ID
@app_views.route(
    "/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


# Route to create a new state
@app_views.route("/states", methods=['POST'], strict_slashes=False)
def post_state():
    if not request.json or not request.is_json:
        abort(400, 'Not a JSON')
    elif 'name' not in request.json:
        abort(400, 'Missing name')
    else:
        new_state = State(**request.get_json())
        new_state.save()
        return jsonify(new_state.to_dict()), 201


# Route to update an existing state by ID
@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    elif not request.json or not request.is_json:
        abort(400, 'Not a JSON')
    else:
        ignore = ['id', 'created_at', 'updated_at']
        for key, value in request.get_json().items():
            if key not in ignore:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict())