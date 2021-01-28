#!/usr/bin/python3
"""states"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def retrobj(state_id=None):
    """retrieve object"""
    if state_id is None:
        Nstatelist = []
        for item in storage.all(State).values():
            Nstatelist.append(item.to_dict())
        return jsonify(Nstatelist)
    elif storage.get(State, state_id):
        return jsonify(storage.get(State, state_id).to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delobj(state_id=None):
    """retrieve object"""
    if storage.get(State, state_id):
        storage.delete(storage.get(State, state_id))
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """post method"""

    if request.get_json() is None:
        abort("Not a JSON", 400)
    elif "name" not in request.get_json().keys():
        abort("Missing name", 400)
    else:
        new_value = State(**request.get_json())
        storage.new(new_value)
        storage.save()
    return jsonify(new_value.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states(state_id):
    """PUT method"""
    if storage.get(State, state_id) is None:
        abort(404)
    if request.get_json() is None:
        abort("Not a JSON", 400)
    if "name" not in request.get_json().keys():
        abort("Missing name", 400)
    for key, value in request.get_json().items():
        if key in ["id", "created_at", "updated_at"]:
            pass
        else:
            setattr(storage.get(State, state_id), key, value)
    storage.save()
    return jsonify(storage.get(State, state_id).to_dict()), 200
