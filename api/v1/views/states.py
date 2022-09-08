#!/usr/bin/python3
"""
State instance 
"""

from flask import Flask, jsonify, request, abort, make_response
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

    state = storage.get("State", state_id)
    
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())

@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_state(state_id):
    """
    Deletes a State object
    """
    state = storage.get("State", state_id)
    
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        # storage.save()
        return make_response(jsonify({}), 200)

@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    Creates a State
    """
    
    body = request.get_json()
    
    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in body.keys():
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        state = State(**body)
        # state.save()
        return make_response(jsonify(state.to_dict()), 201)
    
@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object
    """
    
    body = request.get_json()
    
    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    state = storage.get("State", state_id)
    
    if state is None:
        abort(404)
    else:
        for key, value in body.items():
            print(key)
            return key
            

