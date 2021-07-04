#!/usr/bin/python3
"""function to create the route status"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states')
def states():
    """retrieve all objs"""
    states = []
    for val in storage.all("State").values():
        states.append(val.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>')
def states_id(state_id):
    """get state with his id"""
    for val in storage.all("State").values():
        if val.id == state_id:
            return jsonify(val.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def states_delete(state_id):
    """delete a obj with his id"""
    states = storage.get("State", state_id)
    if states is None:
        abort(404)
    storage.delete(states)
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def states_create():
    """create state"""
    if request.is_json:
        data = request.get_json()
    else:
        msg = "Not a JSON"
        return jsonify({"error": msg}), 400

    if "name" not in data:
        msg = "Missing name"
        return jsonify({"error": msg}), 400

    var = State(**data)
    storage.new(var)
    storage.save()
    return jsonify(var.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def states_update(state_id):
    """update state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if request.is_json:
        data = request.get_json()
    else:
        msg = "Not a JSON"
        return jsonify({"error": msg}), 400

    for k, v in data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(state, k, v)

    storage.save()
    return jsonify(state.to_dict()), 200
