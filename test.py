#!/usr/bin/python3
""" Create a view for the State Objects """


from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify


def all_states():
    states = storage.all(State)
    state_list = [state.to_dict() for state in states.values()]  # Convert each object to dict
    return jsonify(state_list)  # Return JSON response
