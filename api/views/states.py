#!/usr/bin/python3
"""RESTful api actions"""

from flask import request, jsonify
from flask import abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states")
def all_states():
    """Retrieves a list of all state objects"""
    states = storage.all("State")
    all_states = [state.to_dict() for state in states.values()]
    return jsonify(all_states)

@app_views.route("/states", methods=['POST'])
def create_state():
    """create and add a state to states"""
    data = request.get_json()
    if not data:
        result = {"error": "Not a JSON"}
        return jsonify(result), 400
    
    name = data.get("name", None)
    if not name:
        result = {"error": "Missing name"}
        return jsonify(result), 400
    
    for state in storage.all("State").values():
        if state.name == name:
            setattr(state, "name", name)
            state.save()
            result = state.to_dict()
            return jsonify(), 

    state = State(**data)
    state.save()
    result = state.to_dict()
    return jsonify(result), 201

@app_views.route("/states/<state_id>", methods=['GET', 'PUT', 'DELETE'], \
                 strict_slashes=False)
def modify_state(state_id):
    """GET, UPDATE or DELETE state object based on id  else, 400"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    if request.method == "PUT":
        data = request.getjson()
        if not data:
            result = {"Error": "Not a JSON"}
            return jsonify(result), 400
        
        [setattr(state, key, value) for key, value in data.items() \
                if key not in ["id", "created_at", "updated_at"]]
        state.save()

    if request.method =="DELETE":
        state.delete()
        storage.save()
        return jsonify({}), 200

    result = {state.to_dict()}
    return jsonify(result.state), 200