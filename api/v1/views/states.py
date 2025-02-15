#!/usr/bin/python3
"""view for state objects"""

from models import storage
from flask import Flask, abort, jsonify, request
from api/v1/views import app_views
from models.state import State


@app_views.route("/states/<state_id>", methods=["GET", "PUT", "DELETE"])
@app_views.route("/states", methods=["GET", "POST"])
def define_states(state_id=None):
    if request.method == "GET" and state_id is None:
        state_all = storage.all("State")
        state_json = [val.to_dict() for val in state_all.values()]
        return jsonify(state_json)

    state_all = storage.all("State")
    state_key = f"State.{str(state_id)}"
    if state_key in state_all:
        obj = state_all[state_key]
    else:
        abort(404)
        
    if state_id and request.method == "GET":
        return jsonify(obj.to_dict())

    if state_id and request.method == "DELETE":
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200

    if request.method == "POST":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if "name" not in data:
            abort(400, "Missing name")

        new_state = State(**data)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201
    if request.method == "PUT" and state_id:
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        ignored_keys = {"id", "created_at", "updated_at"}
        for key, value in data.items():
            if key not in ignored_keys:
                setattr(obj, key, value)
        storage.save()
        return jsonify(obj.to_dict()), 200
