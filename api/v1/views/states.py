#!/usr/bin/python3
"""
    This Module contains the routes for the CRUD
    for the states
"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import abort, jsonify, request


@app_views.route('/states/', strict_slashes=True)
def states():
    states = [state.to_dict() for state in storage.all("State").values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=True, methods=["GET"])
def get_states(state_id):
    for state in storage.all(State).values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', strict_slashes=True, methods=["DELETE"])
def delete_states(state_id):
    for state in storage.all(State).values():
        if state.id == state_id:
            state.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states/', strict_slashes=True, methods=["POST"])
def post_states():
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data.keys():
        return jsonify({"error": "Missing JSON"}), 400
    obj = State(**data)
    print(obj)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=True, methods=["PUT"])
def put_states(state_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for state_obj in storage.all(State).values():
        if state_id == state_obj.id:
            state = state_obj.to_dict()
            storage.delete(state_obj)
            for key in data.keys():
                if key not in ["id", "updated_at"]:
                    state[key] = data[key]
            state_obj = State(**state)
            storage.new(state_obj)
            state_obj.save()
            return jsonify(state), 200
    abort(404)
