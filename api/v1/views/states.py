#!/usr/bin/python3

"""
State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    states = storage.all(State).values()
    states_list = [state.to_dict() for state in states]
    return jsonify(states_list)

