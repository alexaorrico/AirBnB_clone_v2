#!/user/bin/python3
"""
States file for APi project
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('/states/')
def list_states():
    """lists all states"""
    s_list = []
    states = storage.all("State")
    for state in states.values():
        list.append(state.to_dict)
    return(jsonify(s_list))
