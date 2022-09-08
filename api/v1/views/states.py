#!/usr/bin/python3
"""
State instance 
"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state():
    """
    Retrieves the list of all State objects
    """
    
    states = []
    
    for state in storage.all("State").values():
        states.append(state.to_dict())
        
    return jsonify(states)
        
@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    Retrieves the list of all State objects
    """

    for state in storage.all("State").values():
        if state_id == State.id:
            return jsonify(state.to_dict()):
    
    abort(404)
    
        
        
