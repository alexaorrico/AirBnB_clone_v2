#!/usr/bin/python3
"""Module states"""
from flask import *
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False,
                 defaults={'state_id': None})
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False,)
def get_states(state_id):
    """Retrieves state object"""
    if state_id is None:
        list_obj = []
        for i in storage.all('State').values():
            list_obj.append(i.to_dict())
        return jsonify(list_obj)
    save = storage.get(State, state_id)
    if not save:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(save.to_dict())


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_state(state_id=None):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if not state:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def post_state():
    """POST /api/v1/states"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    s = State(**data)
    s.save()
    return make_response(jsonify(s.to_dict()), 201)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def put_state(state_id=None):
    """Updates a State object"""
    state = storage.get(State, state_id)
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignore_keys = ["id", "created_at", "updated_at"]
    if not state:
        return make_response(jsonify({"error": "Not found"}), 404)
    else:
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
