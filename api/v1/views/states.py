#!/usr/bin/python3
"""Configure API options for State object"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def get_all_states():
    # Return json versions of all states
    state_list = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(state_list)


@app_views.route("/states/<state_id>", strict_slashes=False)
def get_one_state(state_id):
    # Get one state using the get method
    one_state = storage.get(State, state_id)
    if one_state:
        return jsonify(one_state.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_one_state(state_id):
    # Delete a state using the delete method
    to_delete = storage.get(State, state_id)
    if to_delete:
        storage.delete(to_delete)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    state = State(**request.get_json())
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
