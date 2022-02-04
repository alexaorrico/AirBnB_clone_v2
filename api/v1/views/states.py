#!/bin/usr/python3
"""view for State objects"""
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def all_states():
    """Retrieves the list of all State"""
    states = storage.all('State')
    new_list = []
    for state in states.values():
        new_list.append(state.to_dict())
    return jsonify(new_list)
