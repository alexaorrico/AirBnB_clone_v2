#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/states/')
def all_states():
    """
    Return list of the all states
    """
    states_list = []
    states_obj = storage.all("State")
    for _,value in states_obj.items():
        states_list.append(value.to_dict())
    return jsonify(states_list)


