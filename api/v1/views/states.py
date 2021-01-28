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
        for i in storage.all(State).values():
            Nstatelist.append(i.to_dict())
        return jsonify(Nstatelist)
    elif storage.get(State, state_id):
        return jsonify(storage.get(State, state_id).to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delobj(state_id=None):
    """retrieve object"""
    if storage.get(State, state_id):
        storage.delete(storage.get(State, state_id))
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """post method"""
    a = request.get_json()
    if a is None:
        abort("Not a JSON", 400)
    elif "name" not in a.keys():
        abort("Missing name", 400)
    else:
        new_value = State(**a)
        storage.save()
    return jsonify(new_value.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states(state_id):
    """PUT method"""
    a = request.get_json()
    b = storage.get("State", state_id)
    if b is None:
        abort(404)
    if a is None:
        return "Not a JSON", 400
    for key, value in a.items():
        if key in ["id", "created_at", "updated_at"]:
            pass
        else:
            setattr(b, key, value)
    storage.save()
    return jsonify(b.to_dict()), 200
