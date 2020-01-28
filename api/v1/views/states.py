#!/usr/bin/python3
from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """retrieves all State objects"""
    state_list = []
    states = storage.all('State').values()
    for state in states:
        state_list.append(state.to_dict())
    return (jsonify(state_list))


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """Retrieves a single state based on state_id"""
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404)
    else:
        return (jsonify(state_obj.to_dict()))


@app_views.route("/states/<state_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state by ID"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return (jsonify({})), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_state():
    """create a state"""
    if request.get_json is False:
        return (jsonify({"error": "Not a JSON"})), 400
    if "name" not in request.get_json():
        return (jsonify({"error": "Missing name"})), 400
    new_state = State(**request.get_json())
    new_state.save()
    return (new_state.to_dict()), 201


@app_views.route("/states/<state_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id):
    """updates a state object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"})), 400
    for k, v in request.get_json().items():
        if k != "id" and k != "created_at" and k != "updated_at":
            setattr(state, k, v)
    storage.save()
    return (jsonify(state.to_dict())), 200
