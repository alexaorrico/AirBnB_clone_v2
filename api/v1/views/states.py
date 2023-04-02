#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    if states is None:
        abort(404)
    return jsonify([state.to_dict() for state in states])


@app_views.route("/states/<string:state_id>", strict_slashes=False)
def get_state_by_id(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id).to_dict()
    if state is None:
        abort(404)
    return jsonify(state), 200


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state_by_id(state_id):
    """Deletes a State object"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in request.get_json:
        abort(400, "Missing name")
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state_by_id(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
