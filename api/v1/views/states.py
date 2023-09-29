#!/usr/bin/python3
"""api end point
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def all_states():
    """returns all states in the database"""
    states = storage.all("State")

    states_list = [state.to_dict() for state in states.values()]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', strict_slashes=False)
def state_with_id(state_id=None):
    """returns the state ithe the corresponding state id"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id=None):
    """delete state with the corresponding state id"""
    if not state_id:
        abort(404)
    state = storage.get("State", state_id)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state():
    """add a state to the database"""
    try:
        data = request.get_json()
    except Exception as error:
        abort(400, "Not a JSON")

    if "name" not in data:
        return make_response("Missing name", 400)

    new = State(**data)
    storage.new(new)
    storage.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def put_state(state_id=None):
    """modify a state data with the corresponding id"""
    if not state_id:
        abort(404)
    try:
        data = request.get_json()
    except Exception as error:
        abort(400, "Not a JSON")

    state = storage.get("State", state_id)
    if not state:
        abort(404)

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
