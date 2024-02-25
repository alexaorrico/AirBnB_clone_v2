#!/usr/bin/python3
"""
States view
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    state_list = [
        state.to_dict() for state in storage.all("State").values()
        ]
    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=["GET"],
                 strict_slashes=False)
def get_state(state_id):
    """Retrieves a specific State object by ID"""
    state_obj = storage.get("State", str(state_id))
    if state_obj is None:
        abort(404)
    return jsonify(state_obj.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a specific State object by ID"""
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return jsonify({})


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a new State object"""
    state_data = request.get_json(silent=True)
    if state_data is None:
        abort(400, "Not a JSON")

    if "name" not in state_data:
        abort(400, "Missing name")

    new_state = State(**state_data)
    new_state.save()

    resp = jsonify(new_state.to_dict())
    resp.status_code = 201
    return resp


@app_views.route("/states/<state_id>", methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id):
    """Updates a specific State object by ID"""
    state_data = request.get_json(silent=True)
    if state_data is None:
        abort(400, "Not a JSON")

    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)

    for key, value in state_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state_obj, key, value)

    state_obj.save()

    resp = jsonify(state_obj.to_dict())
    resp.status_code = 200
    return resp
