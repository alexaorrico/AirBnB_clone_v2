#!/usr/bin/python3
"""handles actions for states objects"""
from flask import abort, jsonify, request, make_response
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route("/states", strict_slashes=False, methods=["GET"])
@app_views.route("/states/<string:state_id>", strict_slashes=False, methods=["GET"])
def get_state(state_id=None):
    """retrives information about states"""
    if (state_id):
        required_state = storage.get(State, state_id)
        if (not required_state):
            abort(404)
        return jsonify( required_state.to_dict())
    else:
        states = storage.all(State)
        result = []
        for s in states.values():
            result.append(s.to_dict())
        return jsonify(result)


@app_views.route("/states/<string:state_id>", strict_slashes=False, methods=["DELETE"])
def delete_state(state_id):
    """deletes a state"""
    required_state = storage.get(State, state_id)
    if (not required_state):
        abort(404)
    storage.delete(required_state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    """Creates a new state"""
    if not request.json:
        return make_response("Not a JSON", 400)
    if not 'name' in request.json:
        return make_response("Missing name", 400)
    instance = State(**(request.get_json()))
    instance.save()
    return instance.to_dict(), 201


@app_views.route("/states/<string:state_id>", strict_slashes=False, methods=["PUT"])
def edit_state(state_id):
    """edits a state"""
    required_state = storage.get(State, state_id)
    if (not required_state):
        abort(404)
    if not request.json:
        return make_response("Not a JSON", 400)

    input_dict = request.get_json()
    for key, value in input_dict.items():
        if (key not in ["id", "created_at", "updated_at"]):
            if (hasattr(required_state, key)):
                setattr(required_state, key, value)
    required_state.save()
    return required_state.to_dict(), 200
