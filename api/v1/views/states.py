#!/usr/bin/python3
""" module that handles all default RestFul API actions
"""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/states", strict_slashes=False)
def get_states():
    """ get all state objects """
    objs = storage.all("State")
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """ get state object """
    obj = storage.get("State", state_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """delete state object"""
    obj = storage.get("State", state_id)
    if obj:
        obj.delete()
        return jsonify({}), 200
    abort(404)


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def post_state():
    """create state instance"""
    request_dict = request.get_json()
    if not request_dict:
        abort(400)
    state_name = request_dict["name"]
    if not state_name:
        abort(400)
    obj = State(**request_dict)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['PUT'])
def put_state(state_id):
    """update state object"""
    obj = storage.get("State", state_id)
    if not obj:
        abort(404)
    request_dict = request.get_json()
    if not request_dict:
        abort(400)
    for key, value in request_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    return jsonify(obj.to_dict()), 200
