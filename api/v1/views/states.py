#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, Blueprint, render_template, abort, request
from models import storage
from models.state import State
from models.base_model import BaseModel


@app_views.route("/State", methods=["GET", "POST"],
                 strict_slashes=False)
def get_states():
    res = []
    if request.method == "GET":
        for state in storage.all(State).values():
            res.append(state.to_dict())
        return jsonify(res)
    if request.method == "POST":
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in request.json:
            return jsonify({"error": "Missing name"}), 400
        new_state = State(**request.json)
        new_state.save()
        return (jsonify(new_state.to_dict()), 201)


@app_views.route("/State/<state_id>", methods=["GET", "PUT"],
                 strict_slashes=False)
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == "GET":
        return jsonify(state.to_dict())
    if request.method == "PUT":
        print("test\n")
        if not request.json:
            abort(400, description="Not a JSON")
        for key, value in request.json.items():
            setattr(state, key, value)
        state.save()
        return (jsonify(state.to_dict()), 200)


@app_views.route("/State/<state_id>", methods=["Get", "DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == "GET":
        return jsonify(state.to_dict())
    if request.method == "DELETE":
        storage.delete(state)
        storage.save()
        return (jsonify({}), 200)
