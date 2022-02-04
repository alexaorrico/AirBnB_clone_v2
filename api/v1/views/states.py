#!/usr/bin/python3
"""
View for States that handles all RESTful API actions
"""
from models import storage
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def states_all():
    """ test"""
    states_all = []
    states = storage.all("States").values()
    for state in states:
        states_all.append(state.to_dict())
    
    return jsonify(states_all)
