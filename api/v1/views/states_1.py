#!/usr/bin/python3
"""
View for States objects that
handles all default RESTFul AIP Actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"],
                 strict_slashes=False)
def states():
    """Retrieves the list of all State objects"""
    all_states = storage.all(State)
    return jsonify([state.to_dict() for state in all_states.values()])


@app_views.route("/states/<state_id>", methods=["GET"],
                 strict_slashes=False)
def with_state_id(state_id):
    """Retrieves a State Object based on its id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    empty_dict = {}
    return make_response(jsonify(empty_dict), 200)


@app_views.route("/states", methods=["POST"],
                 strict_slashes=False)
def create_state():
    """Creates a State"""
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")
    if "name" not in new_state:
        abort(400, "Missing name")

    state = State(**new_state)
    storage.new(state)
    storage.save()
    data = state.to_dict()
    return make_response(jsonify(data), 201)


@app_views.route("/states/<state_id>", methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    keys_to_ignore = ["id", "created_at", "updated_at"]

    for key, value in body_request.items():
        if key not in keys_to_ignore and hasattr(state, key):
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
