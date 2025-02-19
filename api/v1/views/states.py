#!/usr/bin/python3
""" index routes """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route("/states")
def get_states():
    """get all states"""
    res = []
    for v in storage.all(State).values():
        res.append(v.to_dict())
    return jsonify(res)


@app_views.route("/states/<state_id>")
def get_state(state_id):
    """get state"""
    res = storage.get(State, state_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """delete state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"])
def create_data():
    """add new state"""
    if request.json is None:
        abort(400, "Not a JSON")
    data = request.get_json()
    if "name" not in data:
        abort(400, "Missing name")
    e = State(name=request.json['name'])
    # e = State(**data)
    e.save()
    return jsonify(e.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """update state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
