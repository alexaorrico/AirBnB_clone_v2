#!/usr/bin/python3
"""State objects that handles all default RestFul API actions
"""
from console import *
from models import storage
from models.state import State 
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views

@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states():
    """ route from states"""
    obj_dict = storage.all("State")
    return jsonify([state.to_dict() for state in obj_dict.values()])

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a State object"""
    if request.get_json() is None:
        return "Not a JSON", 400
    elif 'name' not in request.get_json():
        return "Missing name", 400
    else:
        state = State(**request.get_json())
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieve a specific state object by id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """ """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    elif state:
        storage.delete(state)
        storage.save()
    return jsonify({}), 200

@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def up_state(state_id):
    """Create a State object"""
    if request.get_json() is None:
        return "Not a JSON", 400
    state = storage.get(State, state_id)
    if state:
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in request.get_json().items():
            if key not in ignore_keys:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
