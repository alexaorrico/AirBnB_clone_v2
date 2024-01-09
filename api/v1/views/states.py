#!/usr/bin/python3
"""handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, request, jsonify


@app_views.route("/states", strictslashes=False, methods=["GET"])
@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def states(state_id=None):
    states_list = []
    if state_id is None:
        objs = storage.all(State).values()
        for obj in objs:
            states_list.append(obj.to_dict())
        return states_list
    else:
        res = storage.get(State, state_id)
        if res is None:
            abort(404)
        return jsonify(res.to_dict())


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_state(state_id):
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    obj.name = data.get("name", obj.name)
    obj.save()
    return jsonify(obj.to_dict()), 200
