#!/usr/bin/python3
"""Flask route for state model"""

from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET', 'POST'])
def states():
    """route to return all states"""
    if request.method == "GET":
        states_dict = storage.all(State)
        states_list = [obj.to_dict() for obj in states_dict.values()]
        return jsonify(states_list)

    if request.method == "POST":
        request_json = request.get_json()
        if request_json is None:
            abort(400, "Not a JSON")
        if request_json.get("name") is None:
            abort(400, "Missing name")

        newState = State(**request_json)
        newState.save()
        return make_response(jsonify(newState.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"])
def state(state_id=None):
    """Get, update or delete state with state id"""
    state_obj = storage.get(State, state_id)

    if state_obj is None:
        abort(404, "Not found")

    if request.method == "GET":
        return jsonify(state_obj.to_dict())

    if request.method == "DELETE":
        state_obj.delete()
        storage.save()
        return jsonify({})

    if request.method == "PUT":
        request_json = request.get_json()
        if request_json is None:
            abort(400, "Not a JSON")
        state_obj.update(request_json)
        return make_response(jsonify(state_obj.to_dict()), 200)
