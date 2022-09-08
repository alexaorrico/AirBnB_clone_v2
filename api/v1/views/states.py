#!/usr/bin/python3
"""
State instance 
"""

from flask import Flask, jsonify, request
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
        
    
