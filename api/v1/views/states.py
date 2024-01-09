#!/usr/bin/python3
"""
A  new view for State objects that handles all default RESTFul API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.states import State


@app_view.route('/states', methods=['GET'], strict_slashes=False)
def get_state():
    """returns a json state form
    """
    state_list = [s.to_dict() for s in storage.all('State').values()]
    return jsonify(state_list)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """
    retur state id
    """
    state = storage.get("State", state_id)

    if state is None:
        abort(404)

    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)

def delete_state(state_id):
    """deletes a state"""
    state = storage.get("State", state_id)
    
    if state is None:
        abort(404)

    state.delete()
    state.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates a new state obj"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON file"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        object_data = request.get_json()
        obj = State(**object_data)
        obj.save()
        return jsonify(obj.to_dict()), 201
