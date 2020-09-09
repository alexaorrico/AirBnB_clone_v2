#!/usr/bin/python3
""" Restful API for State objects. """
from flask import jsonify, request
from views import app_views
from models.state import State
from models.storage import storage


@app_views.route("/states", methods=["GET", "POST"])
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
    header_dic = request.headers()
    if "name" is not in body_dic:
       abort(400, description="Missing name")
    if header_dic["Content-Type"] != "application/json":
       abort(400, description="Not a JSON")


@app_views.route("/states/<state_id>", methods=["GET", "DELETE"])
def states_id(state_id):
    """ Retrieves a State object using an id. """
    state_objs = storage.all(State)
    state_obj = state_objs.get("State.{}".format(state_id), None)
    if state_obj:
        if request.method == "GET":
            return jsonify(state_obj.to_dict())
        state_obj.delete()
        return jsonify({}), 200  #  method = DELETE
    abort(404)  # when the id is not linked with any state
