#!/usr/bin/python3
""" Restful API for State objects. """
from flask import jsonify
from views import app_views
from models.state import State
from models.storage import storage


@app_views.route("/states", methods=["GET"])
def states_list():
    """ Retrieves a list with all states. """
    state_objs = storage.all(State).values()
    list_dic_states = []
    for state in state_objs:
        list_dic_states.append(state.to_dict())
    return jsonify(list_dic_states)
