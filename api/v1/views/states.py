#!/usr/bin/python3
"""states routes"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, request, abort


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def getStates():
    if request.method == 'GET':
        res = []
        for state in storage.all("State").values():
            res.append(state.to_dict())
        return jsonify(res)
    elif request.method == 'POST':
        state_dict = request.get_json()
        if not state_dict:
            abort(400, "Not a JSON")
        if 'name' not in state_dict.keys():
            abort(400, "Missing name")
        state = State(**state_dict)
        storage.new(state)
        storage.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state_by_id(state_id):
    print(state_id)
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        update_dict = request.get_json()
        if not update_dict:
            abort(400, "Not a JSON")
        for key in update_dict:
            if key not in ['created_at', 'id', 'updated_at']:
                setattr(state, key, update_dict[key])
        state.save()
        return jsonify(state.to_dict()), 200
