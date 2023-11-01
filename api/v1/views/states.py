#!/usr/bin/python3
"""states  added to the database and states removed from the database"""

from flask import jsonify, request, abort
from . import app_views, State, storage

pl = ("name",)


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def post_states():
    """Adds a new state to the list of states available on the server."""
    if request.method == "GET":
        return jsonify([list.to_dict()
                        for list in storage.all(State).values()])
    else:
        data = request.get_json(silent=True)
        if request.is_json and data is not None:
            load = {key: str(value) for key, value in data.items()
                    if key in pl}
            if not load.get("name", None):
                abort(400, description="Missing name")
            added_state = State(**load)
            storage.new(added_state), storage.save()
            return jsonify(added_state.to_dict()), 201
        abort(400, description="Not a JSON")


@app_views.route("/states/<state_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def delete_state(state_id):
    """"Removes a state from the list of states linked to the provided ID"""
    info = storage.get(State, str(state_id))
    if not info:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify(info.to_dict())
    elif request.method == "DELETE":
        storage.delete(info), storage.save()
        return jsonify({})
    else:
        data = request.get_json(silent=True)
        if request.is_json and data:
            [setattr(info, key, str(value)) for key, value in data.items()
             if key in pl]
            info.save()
            return jsonify(info.to_dict()), 200
        abort(400, description="Not a JSON")
