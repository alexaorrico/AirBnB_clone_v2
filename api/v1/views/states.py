#!/usr/bin/env python3
"""Defines an api that gets all State object"""

from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def states():
    """Return the list of all State objects"""
    all = storage.all("State")
    states = all.values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=["GET"],
                 strict_slashes=False)
def state(state_id):
    """Return a particular state"""
    state = storage.get(State, state_id)
    if state == "None":
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(state_id):
    """Delete a state with a particular id from database"""
    state = storage.get("State", state_id)
    print("deleting")
    print(state)
    if state == "None":
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def post():
    """Create and return a new state with status code 201"""
    state = request.get_json()
    if state == "None":
        abort(404, "Not a JSON")
    if 'name' not in state:
        abort(404, "Missing name")
    new_state = State(**state)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put(state_id):
    """Update a State with a particular id in a database"""
    state = storage.get("State", state_id)
    if state == "None":
        abort(404)
    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
