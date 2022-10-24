#!/usr/bin/python3
""" States """

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, state


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getallstate():
    """Gets all states"""
    req = []
    for i in storage.all("State").values():
        req.append(i.to_dict())

    return jsonify(req)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getstate(state_id=None):
    """Gets a state"""
    stat = storage.get("State", state_id)
    if stat is None:
        abort(404)
    else:
        return jsonify(stat.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletestate(state_id=None):
    """Deletes a state"""
    stat = storage.get("State", state_id)
    if stat is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def createstate():
    """Create a state"""
    stat = request.get_json(silent=True)
    if stat is None:
        abort(400, "Not a JSON")
    elif "name" not in stat.keys():
        abort(400, "Missing name")
    else:
        new_stat = state.State(**s)
        storage.new(new_stat)
        storage.save()
        return jsonify(new_stat.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updatestate(state_id=None):
    """Update a state"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)

    stat = request.get_json(silent=True)
    if stat is None:
        abort(400, "Not a JSON")
    else:
        for x, y in stat.items():
            if x in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(obj, x, y)
        storage.save()
        req = obj.to_dict()
        return jsonify(req), 200
