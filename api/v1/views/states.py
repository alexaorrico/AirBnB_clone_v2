#!/usr/bin/python3
"""script to serve routes related to states objects"""
from models.state import State
from models import storage
from api.v1.views import app_views
import json

from flask import request, jsonify, abort

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def serve_states():
    """Retrieves a list of all State objects"""
    states = storage.all(State)
    list_states = [ state.to_dict() for state in states.values()]
    return jsonify(list_states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def serve_state_id(state_id):
    """Retrives a State object"""
    response = storage.get(State, state_id)

    if response is None:
        # return jsonify({"error": "Not found"}), 404
        abort(404)
    
    return jsonify(response.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state_obj(state_id):
    """deletes a State object"""
    # print(f"DELETE API ROUTE")
    state_to_delete = storage.get(State, state_id)

    if state_to_delete is None:
        abort(404)
    
    # print(f"\tDELETE instance:{type(state_to_delete)} dict:{state_to_delete.to_dict()}")
    storage.delete(state_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_new_state():
    """creates a State"""

    if request.headers['Content-Type'] == 'application/json':
        data_entered = request.get_json()
        if data_entered is None:
            # NOT WORKING NEEDS REPAIR !!!!!
            abort(400, description="Not a JSON")
    else:
        abort(400, description="Content-Type is not application/json")

    if data_entered.get('name') is None:
        abort(400, description="Missing name")
    
    # if name not in dict
    if data_entered.get('name') is None:
        abort(400, description="Missing name")

    new_state = State(name=data_entered.get('name'))
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201

    
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_obj(state_id):
    """updates a State object"""
    state_to_update = storage.get(State, state_id)

    if state_to_update is None:
        abort(404)

    if request.headers['Content-Type'] == 'application/json':
        data_entered = request.get_json()
        if data_entered is None:
            # NOT WORKING NEEDS REPAIR !!!!!
            abort(400, description="Not a JSON")
    else:
        abort(400, description="Content-Type is not application/json")
    
    for key, value in data_entered.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state_to_update, key, value)
    
    storage.save()

    return jsonify(state_to_update.to_dict()), 200
