#!/usr/bin/python3
"""
states view routes
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route(
    "/states",
    methods=["GET", "POST"],
    strict_slashes=False,
)
def get_states():
    """Handles /states endpoint

    Returns:
        json: list of all states or the newly added state
    """
    if request.method == "POST":
        state_data = request.get_json(silent=True)
        if state_data is None:
            return jsonify(error="Not a JSON"), 400

        if "name" not in state_data:
            return jsonify(error="Missing name"), 400
        else:
            state = State(**state_data)
            storage.new(state)
            storage.save()
            return jsonify(state.to_dict()), 201

    else:
        states = list(storage.all(State).values())
        return jsonify([state.to_dict() for state in states])


@app_views.route(
    "/states/<id>",
    methods=["GET", "DELETE", "PUT"],
    strict_slashes=False,
)
def state(id=None):
    """Handles /states/id endpoint

    Returns:
        json: object for GET, empty dict for DELETE or 404
    """
    state = storage.get(State, id)
    if state is None:
        abort(404)

    if request.method == "DELETE":
        storage.delete(state)
        storage.save()
        return jsonify({})
    elif request.method == "PUT":
        state_data = request.get_json(silent=True)
        if state_data is None:
            return jsonify(error="Not a JSON"), 400

        for key, value in state_data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict())

    else:
        return jsonify(state.to_dict())
