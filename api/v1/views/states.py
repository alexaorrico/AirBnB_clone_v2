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
    obj_states = storage.all(State)
    my_dict = [obj.to_dict() for obj in obj_states.values()]
    if not state_id:
        if request.method == "GET":
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
        if request.method == "GET":
            for state in my_dict:
                if state.get('id') == state_id:
                    return jsonify(state)
            abort(404)
        elif request.method == "DELETE":
            for ob in obj_states.values():
                if ob.id == state_id:
                    storage.delete(ob)
                    storage.save()
                    return jsonify({}), 200
            abort(404)
        elif request.method == "PUT":
            get_new_name = request.get_json()
            if not get_new_name:
                abort(400, "Not a JSON")
            for state in obj_states.values():
                if state.id == state_id:
                    state.name = get_new_name.get("name")
                    state.save()
                    return jsonify(state.to_dict()), 200
            abort(404)
