#!/usr/bin/python3
"""Flask route for state model"""

from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET', 'POST'])
def states_no():
    """route to return all states"""
    state_list = []
    state_obj = storage.get(state, state_id)
    if request.method == "GET":
        if state_id is None:
            obj = storage.all(State).values()
            for new in obj:
                state_list.append(new.to_dict())
            return jsonify(state_list)
        else:
            res = storage.get(State, state_id)
            if res is None:
                abort(404)
            return jsonify(res.to_dict())

    if request.method == "POST":
        request_json = request.get_json()
        if request_json is None:
            abort(400, "Not a JSON")
        if request_json.get("name") is None:
            abort(400, "Missing name")
        newState = State(**request_json)
        newState.save()
        return jsonify(newState.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=[
    "GET", "DELETE", "PUT"])
def state(state_id=None):
    """Get, update or delete state with state id"""
    state_list = []
    state_obj = storage.get(State, state_id)

    if request.method == "GET":
        if state_id is None:
            obj = storage.all(State).values()
            for new in obj:
                state_list.append(new.to_dict())
            return jsonify(state_list)
        else:
            res = storage.get(State, state_id)
            if res is None:
                abort(404)
            return jsonify(res.to_dict())

    if request.method == "DELETE":
        if state_obj is None:
            abort(404)
        storage.delete(state_obj)
        storage.save()
        return jsonify({}), 200

    if request.method == "PUT":
        if state_obj is None:
            abort(400)
        request_json = request.get_json()
        if not request_json:
            abort(400, "Not a JSON")
        state_obj.name = request_json.get("name", state_obj.name)
        state_obj.save()
        return jsonify(state_obj.to_dict()), 200
