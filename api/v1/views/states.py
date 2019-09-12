#!/usr/bin/python3
"""State objects that handles all default RestFul API actions"""

from models.base_model import BaseModel
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/states")
def get_state_route():
    """ Retrieves the list of all State objects """
    states_list = []
    for key, value in BaseModel.to_dict().items():
        if "State" in key:
            states_list.append(value)
    return jsonify(states_list)
