#!/usr/bin/python3
"""states"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from datetime import datetime
import uuid


@app_views.route(
    "/states/",
    methods=["GET"],
    strict_slashes=False,
)
def list_states():
    """Retrieves the list of all State objects"""
    all_states = storage.all("State").values()
    states = [obj.to_dict() for obj in all_states]
    return jsonify(states)


@app_views.route(
    "/states/<state_id>",
    methods=["GET"],
    strict_slashes=False,
)
def get_state(state_id):
    """Retrieves a State object"""
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    return jsonify(state_obj[0])


@app_views.route(
    "/states/<state_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
def delete_state(state_id):
    """Deletes a State object"""
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    storage.delete(state_obj[0])
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/states/",
    methods=["POST"],
    strict_slashes=False,
)
def create_state():
    """Creates a State"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    new_state = State(**request.get_json())
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route(
    "/states/<state_id>",
    methods=["PUT"],
    strict_slashes=False,
)
def updates_state(state_id):
    """Updates a State object"""
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state_obj, key, value)
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200
