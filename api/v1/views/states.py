#!/usr/bin/python3
"""
States view for API
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, state


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getallstate():
    """Gets all states"""
    res = []
    for i in storage.all("State").values():
        res.append(i.to_dict())

    return jsonify(res)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getstate(state_id=None):
    """Gets a state"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    else:
        return jsonify(s.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletestate(state_id=None):
    """Deletes a state"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def createstate():
    """Create a state"""
    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a JSON")
    elif "name" not in s.keys():
        abort(400, "Missing name")
    else:
        new_s = state.State(**s)
        storage.new(new_s)
        storage.save()
        return jsonify(new_s.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updatestate(state_id=None):
    """Update a state"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)

    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a JSON")
    else:
        for k, v in s.items():
            if k in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(obj, k, v)
        storage.save()
        res = obj.to_dict()
        return jsonify(res), 200
