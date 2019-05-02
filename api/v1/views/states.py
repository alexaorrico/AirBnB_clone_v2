#!/usr/bin/python3
"""States view for HBNB API"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State

@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states_get():
    states = [v.to_dict() for k, v in storage.all("State").items()]
    return jsonify(states)

@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_get(state_id):
    state = [v.to_dict() for k, v in
             storage.all("State").items() if k == 'State.' + state_id]
    if not state or len(state) != 1:
        abort(404)
    return jsonify(state[0])

@app_views.route("/states/<state_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def state_delete(state_id):
    state = storage.get(state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route("/states/",
                 methods=["POST"],
                 strict_slashes=False)
def state_post():
    new_dict = request.get_json(silent=True)
    if not new_dict:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    state = State(**new_dict)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

@app_views.route("/states/<state_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def state_put(state_id):
    state_dict = request.get_json(silent=True)
    if not state_dict:
        return jsonify({"error": "Not a JSON"}), 400
    state = storage.get("State", state_id)
    for k, v in state_dict.items():
        if k not in ["id", "updated_at", "created_at"]:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
