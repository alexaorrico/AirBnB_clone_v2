#!/usr/bin/python3
"""Handles all default RestFul API actions for State objects"""

from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.state import State


@app_views.route("/states",
                 methods=['GET', 'DELETE', 'POST', 'PUT'],
                 strict_slashes=False)
@app_views.route("/states/<state_id>",
                 methods=['GET', 'DELETE', 'POST', 'PUT'],
                 strict_slashes=False)
def states_list(state_id=None):
    """Retrieves a list of all State objects"""
    if request.method == 'GET':
        if not state_id:
            states = storage.all("State").values()
            l_1 = []
            for value in states:
                d = value.to_dict()
                l_1.append(d)
            return jsonify(l_1)
        else:
            state = storage.get("State", state_id)
            if not state:
                abort(404)
            return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        state = storage.get("State", state_id)
        if not state:
            abort(404)
        state.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'POST':
        dic = request.get_json()
        if not dic:
            return 'Not a JSON', 400
        if "name" not in dic.keys():
            return 'Missing name', 400
        s = State(**dic)
        s.save()
        return jsonify(s.to_dict()), 201
    elif request.method == 'PUT':
        state = storage.get("State", state_id)
        if state is None:
            abort(404)
        dic = request.get_json()
        if not dic:
            return 'Not a JSON', 400
        for k, v in dic.items():
            if k != "id" or k != "created_at" or k != "updated_at":
                setattr(state, k, v)
        state.save()
        return jsonify(state.to_dict())
