#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API actions
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    all_states = storage.all("State").values()
    result = [state.to_dict() for state in all_states]
    return jsonify(result), 200


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get("State", str(state_id))
    if state is None:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get("State", str(state_id))
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return ({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a State"""
    state_dict = request.get_json(silent=True)
    if state_dict is None:
        abort(400, "Not a JSON")
    if "name" not in state_dict:
        abort(400, "Missing name")

    state_inst = State(**state_dict)
    state_inst.save()
    return jsonify(state_inst.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state_obj = storage.get("State", str(state_id))
    state_dict = request.get_json(silent=True)
    if state_obj is None:
        abort(404)
    if state_dict is None:
        abort(400, "Not a JSON")
    for key, val in state_dict.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state_obj, key, val)
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200

# get the object to be updated by it's id
# get the dictionary repr of state instance for id=state_id using get_json()
# check if it's a valid json and return none if it's not
# iterate the dictionary
# id, created_at and updated_at should not be available to be set
# set object attributes based on their keys
