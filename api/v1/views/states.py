#!/usr/bin/python3
"""State module"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, request, abort


@app_views.route("/states", methods=["GET"])
def get_state():
    """Gets state objects"""
    state_list = []
    for i in storage.all(State).values():
        state_list.append(i.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state_id(state_id):
    """Gets a certain state based on the state's id"""
    if storage.get(State, state_id) is None:
        abort(404)
    else:
        return (jsonify(storage.get(State, state_id).to_dict()))


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Deletes a state based on id"""
    all_the_states = storage.get(State, state_id)
    if all_the_states is None:
        abort(404)
    else:
        storage.delete(all_the_states)
        storage.save()
        return (jsonify({})), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_state():
    """Creates a new state object"""
    data = request.get_json()
    if not data:
        return (jsonify({"error": "Not a JSON"})), 400
    if "name" not in data:
        return (jsonify({"error": "Missing name"})), 400
    new_state_obj = State(**data)
    new_state_obj.save()
    return (new_state_obj.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates the state object"""
    data = request.get_json()
    all_the_states = storage.get(State, state_id)
    if all_the_states is None:
        abort(404)
    if not data:
        return (jsonify({"error": "Not a JSON"})), 400
    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(all_the_states, key, value)
    storage.save()
    return (jsonify(all_the_states.to_dict())), 200
