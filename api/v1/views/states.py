#!/usr/bin/python3
"""states"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """get state object"""
    if state_id is None:
        Nstatelist = []
        for item in storage.all(State).values():
            Nstatelist.append(item.to_dict())
        return jsonify(Nstatelist)
    elif storage.get(State, state_id):
        return jsonify(storage.get(State, state_id).to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_state(state_id=None):
    """Delete state object"""
    if storage.get(State, state_id):
        storage.delete(storage.get(State, state_id))
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Add state object"""
    if request.get_json() is None:
        abort(400, "Not a JSON")
    elif "name" not in request.get_json().keys():
        abort(400, "Missing name")
    else:
        new_state = State(**request.get_json())
        storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id=None):
    """Update state object"""
    if storage.get("State", state_id) is None:
        abort(404)
    if request.get_json() is None:
        return "Not a JSON", 400
    for key, value in request.get_json().items():
        if key in ["id", "created_at", "updated_at"]:
            pass
        else:
            setattr(storage.get("State", state_id), key, value)
    storage.save()
    return jsonify(storage.get("State", state_id).to_dict()), 200
