#!/usr/bin/python3
"""
-------------------------------------------------------------------------------
MODULE NAME: states
-------------------------------------------------------------------------------
"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import abort, jsonify, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Return all states"""
    return jsonify(list(map(lambda x: x.to_dict(),
                            storage.all(State).values())))


@app_views.route('states/<state_id>', methods=['GET'], strict_slashes=False)
def state(state_id):
    """Return information of a state"""
    try:
        return jsonify(storage.get(State, state_id).to_dict())
    except Exception:
        abort(404)


@app_views.route('states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete a state and return a empty dictionary"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    state.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new state"""
    json_state = request.get_json()
    if json_state is None:
        abort(400, "Not a JSON")
    elif "name" not in json_state.keys():
        abort(400, "Missing name")
    else:
        state = State(**json_state)
        state.save()
        return (state.to_dict()), 201


@app_views.route('states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a state by id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    new_json = request.get_json()
    if new_json is None:
        abort(400, "Not a JSON")

    for key, value in new_json.items():
        if key not in ("id", "created_at", "updated_at"):
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200
