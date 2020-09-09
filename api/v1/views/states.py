#!/usr/bin/python3
""" Restful API for State objects. """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route("/states",
                 methods=["GET", "POST"], strict_slashes=False)
def states_list():
    """ Retrieves a list with all states. """
    if request.method == "GET":
        state_objs = storage.all(State).values()
        list_dic_states = []
        for state in state_objs:
            list_dic_states.append(state.to_dict())
            return jsonify(list_dic_states)
    # method is POST
    body_dic = request.get_json()
    if "name" not in body_dic:
        return jsonify(error="Missing name"), 400
    if body_dic is None:
        return jsonify(error="Not a JSON"), 400
    new_state = State(body_dic)
    storage.new(new_state)
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>",
                 methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def states_id(state_id):
    """ Retrieves a State object using an id. """
    state_objs = storage.all(State)
    state_obj = state_objs.get("State.{}".format(state_id), None)
    if state_obj:
        if request.method == "GET":
            return jsonify(state_obj.to_dict())
        if request.method == "DELETE":
            state_obj.delete()
            return jsonify({}), 200
        else:  # method = PUT
            body_dic = request.get_json()
            if body_dic is None:
                return jsonify(error="Not a JSON"), 400
            for key, value in state_objs.items():
                ignore_keys = ["id", "created_at", "updated_at"]
                if key not in ignore_keys:
                    setattr(state_objs, key, value)
            storage.save()
            return jsonify(state_object.to_dict()), 200
    abort(404)  # when the id is not linked with any state
