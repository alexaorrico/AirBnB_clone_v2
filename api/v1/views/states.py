#!/usr/bin/python3
"""View for State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """return all the states in the database"""
    states_list = []

    for state in storage.all(State).values():
        states_list.append(state.to_dict())

    return states_list
