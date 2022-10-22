#!/usr/bin/python3
"""
Module for state object.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Method getting all the states """
    data = storage.all(State)
    new = [val.to_dict() for key, val in data.items()]
    return jsonify(new)


@app_views.route('/states/,state_id', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """Get individual sate objects"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404, "Not found")
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """delete each states"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404, "Not found")
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id', methods=['POST'], strict_slashes=False)
def create_state():
    """Create  a state not exists"""
    args = request.get_json()
    if not args:
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in args:
        return jsonify({"error": "Missing name"}), 400
    obj = State(**args)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """Update each states"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404, "Not found")
    args = request.get_json()
    if not args:
        return jsonify({"error": "Not a JSon"}), 400
    for key, values in args.items():
        if key not in ["id", "update_at", "created_at"]:
            setattr(obj, key, values)

    obj.save()
    return jsonify(obj.to_dict()), 200
