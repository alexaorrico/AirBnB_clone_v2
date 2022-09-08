#!/usr/bin/python3
"""
State
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/states', methods=['GET'])
def states():
    states = storage.all("State")
    states_list = []
    for state in states.values:
        states_list.append(state.to_dict())
    return(jsonify(states_list))
