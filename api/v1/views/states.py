#!/usr/bin/python3
"""Default restful api actions for state"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_state(state_id=None):
    """Method to retrieve list of all state objects or state object by id"""
    #return "In the right place"
    if state_id is None:
        state_list = []
        for obj in storage.all(State).values():
            state_list.append(obj.to_dict())
        return jsonify(state_list)
        return "State id is None"
    for obj in storage.all(State).values():
        if obj.id == state_id:
            state = obj.to_dict()
            return state
    abort(404)
    