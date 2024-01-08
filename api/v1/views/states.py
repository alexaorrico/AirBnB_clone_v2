#!/usr/bin/python3
"""states"""

from models.state import State
from flask import Flask, abort, jsonify, request
from models import storage
from api.v1.views import app_views

# use strict_slashes because /states is different from /states/
# task asks for /states but example uses /states/


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def get_states():
    """get status method"""
    get = storage.all(State)
    li = []
    for item in get.values():
        li.append(item.to_dict())
    return jsonify(li)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states_by_id(state_id):
    """get states by id"""
    get = storage.get(State, state_id)
    if (get is None):
        abort(404)
    else:
        return jsonify(get.to_dict())


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_states():
    """post status"""
    get_json = request.get_json()
    if not get_json:
        abort(400, "Not a JSON")
    if not get_json.get("name"):
        abort(400, "Missing name")
    # use the json you got to iintialize all object atributes
    # not just the name attribute
    new = State(**get_json)
    storage.new(new)
    storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_states(state_id):
    """delete status"""
    get = storage.get(State, state_id)
    if (get is None):
        abort(404)
    storage.delete(get)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states(state_id):
    """put in status"""
    get = storage.get(State, state_id)
    get_json = request.get_json()
    if not get:
        abort(404)
    if not get_json:
        abort(400, "Not a JSON")
    for item in storage.all(State):
        # easier approach and loops through ALL object attributes,
        # not just the name

        for k, v in get_json.items():
            if k not in ["id", "created_at", "updated_at"]:
                setattr(get, k, v)
    storage.save()
    return jsonify(get.to_dict())
