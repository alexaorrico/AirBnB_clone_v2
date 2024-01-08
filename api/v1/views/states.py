#!/usr/bin/python3
"""states"""

from models.state import State
from flask import Flask, abort, jsonify, request
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'])
def get_states():
    """get status method"""
    get = storage.all(State)
    li = []
    for item in get.values():
        li.append(item.to_dict())
    return jsonify(li)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_states_by_id(state_id):
    get = storage.get(State, state_id)
    if (get is None):
        abort(404)
    else:
        return jsonify(get.to_dict())


@app_views.route('/states', methods=['POST'])
def post_states():
    get_json = request.get_json()
    if not get_json:
        abort(400, "Not a JSON")
    if not get_json.get("name"):
        abort("400", "Missing name")
    new = State({"name": get_json.get("name")})
    storage.new(new)
    storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_states(state_id):
    get = storage.get(State, state_id)
    if (get is None):
        abort(404)
    storage.delete(get)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_states(state_id):
    get = storage.get(State, state_id)
    get_json = request.get_json()
    if not get:
        abort(404)
    if not get_json:
        abort(400, "Not a JSON")
    for item in storage.all(State):
        if (item["id"] == state_id):
            storage.all(State)["State." + state_id]["name"] == get_json["name"]
    storage.save()
    return jsonify(get.to_dict())
