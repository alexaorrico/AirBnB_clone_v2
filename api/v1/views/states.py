#!/usr/bin/python3
"""
States view
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states', methods=["GET"])
def get_state():
    """ Gets a single state
    """
    state_list = []
    state_obj = storage.all("State")
    for obj in state_obj.values():
        state_list.append(obj.to_dict())

    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=["GET"])
def get_states(state_id):
    """ Gets state based on id passed"""
    state_obj = storage.get("State", str(state_id))
    if state_obj is None:
        abort(404)

    return jsonify(state_obj.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def del_state(state_id):
    """ Deletes a state using ID"""
    state_obj = storage.get('State', str(state_id))
    if state_obj is None:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return jsonify({}, 200)


@app_views.route("/states", methods=["POST"])
def create_state():
    """Create a new post"""
    new_state = request.get_json()
    if new_state is None:
        abort(400, "Not a JSON")

    if "name" not in new_state:
        abort(400, "Missing name")

    state_instance = State(**new_state)
    storage.new(state_instance)
    storage.save()
    resp = jsonify(state_instance.to_dict())
    resp.status_code = 201

    return resp


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_states(state_id):
    """Updates an existing state"""
    state_obj = storage.get("State", str(state_id))
    if state_obj is None:
        abort(404)

    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")

    for key, value in new_state.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state_obj, key, value)
    state_obj.save()
    resp = jsonify(state_obj.to_dict())
    resp.status_code = 200
    return resp
