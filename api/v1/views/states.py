#!/usr/bin/python3
from models import storage
from models.state import State
from . import app_views
from flask import jsonify, abort, request

@app_views.route("/states")
def states():
    states = storage.all(State)
    response = []
    for state in states.values():
        response.append(state.to_dict())
    return jsonify(response)

@app_views.route("states/<state_id>")
def state(state_id):
    obj = storage.get(State, state_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)

@app_views.route("states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    obj = storage.get(State, state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)

@app_views.route("/states", methods=["POST"])
def create_state():
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if "name" not in data:
        abort(400, "Missing name")
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201

@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if "id" in data:
        data.pop("id")
    if "created_at" in data:
        data.pop("created_at")
    if "updated_at" in data:
        data.pop("updated_at")
    for key, value in data.items():
        state.__setattr__(key, value)
    state.save()
    return jsonify(state.to_dict())
        