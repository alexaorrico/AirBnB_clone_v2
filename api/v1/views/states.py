#!/usr/bin/python3
"""Defines all routes for the `State` entity
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage, classes


@app_views.route("/states", methods=["GET"])
def get_states():
    """Returns all states in json response"""
    states = []
    states_objs = storage.all("State")
    for state in states_objs.values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route("/states/", methods=["POST"])
def create_state():
    """Creates a new state in storage"""
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, description="Not a JSON")
    if "name" not in data:
        return abort(400, description="Missing name")
    state = classes["State"](**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """Returns a state object or None if not found."""
    state = storage.get("State", state_id)
    return jsonify(state.to_dict()) if state else abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Deletes a state object from storage"""
    state = storage.get("State", state_id)
    if state is None:
        return abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """Update a state object by id"""
    state = storage.get("State", state_id)
    if state is None:
        return abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, description="Not a JSON")

    data.pop("id", None)
    data.pop("updated_at", None)
    data.pop("created_at", None)

    for k, v in data.items():
        setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict())
