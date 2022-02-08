#!/usr/bin/python3
"""create a CRUD for states table"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route("/states", strict_slashes=False)
def get_states():
    """return all rows in a states table"""
    states_list = []
    for i in storage.all(State).values():
        states_list.append(i.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def get_one_state(state_id):
    """return a state_id, if is it None, return not found"""
    if state_id:
        states_dict = storage.all(State)
        for i in states_dict.values():
            if i.id == state_id:
                return jsonify(i.to_dict())
        return abort(404)
    else:
        return


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_one_state(state_id):
    """delete a state_id if exists"""
    if state_id:
        state = storage.get(State, state_id)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=["POST"])
def create_state():
    """create a new row(state)"""
    try:
        state = request.get_json()
        if state.get("name") is None:
            return jsonify({"error": "Missing name"}), 400
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    new_state = State(**state)
    storage.save()
    return jsonify(new_state.to_dict()), 201
