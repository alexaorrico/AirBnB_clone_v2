#!/usr/bin/python3
"""State RESTAPI"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route("/states", strict_slashes=False)
def get_states():  # Get all states
    states = storage.all(State)
    return jsonify([value.to_dict() for _, value in states.items()])


@app_views.route("/states/<string:state_id>", strict_slashes=False)
def get_state(state_id):  # get a specific state
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route("/states/<string:state_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_state(state_id):  # Delete a state
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():  # Create a state
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "name" not in data:
        abort(400, description="Missing name")
    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<string:state_id>",
                 strict_slashes=False, methods=["PUT"])
def update_state(state_id):  # Update a state
    state = storage.get(State, state_id)
    if state:
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state, key, value)
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
    abort(404)
