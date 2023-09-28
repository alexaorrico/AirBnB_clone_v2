#!/usr/bin/python3
"""
Creating new view for State object
that handles all default RestFul API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/', methods=["GET"])
def get_all_states():
    """
    gets all states
    """
    states = []
    for value in storage.all("State").values():
        states.append(value.to_dict())
    return (jsonify(states))


@app_views.route("/states/<state_id>", methods=["GET"])
def state(state_id=None):
    """
    function to retrieve states by id
    """
    if state_id is None:
        states = storage.all("State")
        grabbed_state = [value.to_dict() for key, value in states.items()]
        return (jsonify(grabbed_state))
    grabbed_state = storage.get("State", state_id)
    if grabbed_state is not None:
        return (jsonify(grabbed_state.to_dict()))
    abort(404)


@app_views.route('/states/<state_id>', methods=["DELETE"])
def delete_states(state_id):
    """
    function to delete state by id
    """
    del_state = storage.all("State").values()
    obj = [objct.to_dict() for objct in del_state if objct.id == state_id]
    if obj == []:
        abort(404)
    obj.remove(obj[0])
    for objct in del_state:
        if objct.id == state_id:
            storage.delete(objct)
            storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/', methods=["POST"])
def post_states():
    """
    function to create states
    """
    content = request.get_json()
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    name = content.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    added_state = State()
    added_state.name = name
    added_state.save()

    return (jsonify(added_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=["PUT"], strict_slashes=False)
def update_states(state_id):
    """
    method to update states
    """
    update_state = storage.get("State", state_id)
    if update_state is None:
        abort(404)

    if not request.json:
        return (jsonify({"error": "Not a JSON"}), 400)

    content = request.get_json()

    for key, value in content.items():
        if key != "id" or key != "created_at" or key != "updated_at":
            setattr(update_state, key, value)

    update_state.save()
    return (jsonify(update_state.to_dict()), 200)
