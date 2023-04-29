#!/usr/bin/python3
"""restful API functions for State"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import request, jsonify, abort


@app_views.route("/states",
                 strict_slashes=False,
                 methods=["GET", "POST"]
                 )
@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=["DELETE", "PUT", "GET"])
def state_end_points(state_id=None):
    """to get states"""
    if not state_id:
        obj_states = storage.all(State)
        if request.method == "GET":
            my_dict = [obj.to_dict() for obj in obj_states.values()]
            return jsonify(my_dict)

        elif request.method == "POST":
            imput = request.get_json()
            if not imput:
                abort(400, "Not a JSON")
            elif not imput["name"]:
                abort(400, "Missing name")
            else:
                new_state = State(**imput)
                new_state.save()
                return jsonify(new_state.to_dict()), 201
    else:
        obj_state = storage.get("State", state_id)
        if obj_state is None:
            abort(404)
        if request.method == "GET":
            return jsonify(obj_state.to_dict()), 201
        elif request.method == "DELETE":
            storage.delete(obj_state)
            storage.save()
            return jsonify({}), 200
        elif request.method == "PUT":
            get_new_name = request.get_json()
            if not get_new_name:
                abort(400, "Not a JSON")
            obj_state.name = get_new_name["name"]
            obj_state.save()
            return jsonify(obj_state.to_dict()), 200
