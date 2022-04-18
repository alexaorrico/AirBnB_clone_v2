#!/usr/bin/python3
"""
Creating new view for State object
that handles all default RestFul API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models import State


@app_views.route('/states/', methods=["GET"])
def get_all_states():
    """
    gets all states
    """
    states = []
    for v in storage.all("State").values():
        states.append(v.to_dict())
    return (jsonify(states))


@app_views.route("/states/<state_id>", methods=["GET"])
def state(state_id=None):
    """
    function to retrieve list of all states
    """
    if state_id is None:
        states = storage.all("State")
        get_state = [value.to_dict() for key, value in states.items()]
        return (jsonify(get_state))
    get_state = storage.get("State", state_id)
    if get_state is not None:
        return (jsonify(get_state.to_dict()))
    abort(404)


@app_views.route('/states/<state_id>', methods=["DELETE"])
def delete_states(state_id):
    """
    function to delete state based on id
    """
    del_state = storage.all("State").values()
    obj = [obje.to_dict() for obje in del_state if obje.id == state_id]
    if obj == []:
        abort(404)
    obj.remove(obj[0])
    for obje in del_state:
        if obje.id == state_id:
            storage.delete(obje)
            storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/', methods=["POST"])
def post_states():
    """
    function to add states
    """
    content = request.get_json()
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    name = content.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    add_state = State()
    add_state.name = name
    add_state.save()

    return (jsonify(add_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=["PUT"], strict_slashes=False)
def update_states(state_id):
    """
    function to update states
    """
    set_state = storage.get("State", state_id)
    if set_state is None:
        abort(404)

    if not request.json:
        return (jsonify({"error": "Not a JSON"}), 400)

    content = request.get_json()

    for key, value in content.items():
        if key != "id" or key != "created_at" or key != "updated_at":
            setattr(set_state, key, value)

    set_state.save()
    return (jsonify(set_state.to_dict()), 200)
