#!/usr/bin/python3
"""
index file
"""
import json
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/states", methods=['GET'])
def list_states():
    """
    Retrieves the list of all State objects
    """
    states = storage.all(State).values()
    states_list = [state.to_dict() for state in states]
    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=['GET'])
def retrieve_state(state_id):
    """
    Retrieves a State object
    """
    states = storage.all(State).values()
    states_list = [state.to_dict() for state in states if state.id == state_id]
    if not states_list:
        abort(404)
    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes a State object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'])
def create_state():
    """
    Creates a State
    """
    if not request.get_json():
        return abort(400, {'message': 'Not a JSON'})

    if 'name' not in request.get_json():
        return abort(400, {'message': 'Missing name'})

    new_state = State(**request.get_json())
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'])
def update_state(state_id):
    """
    Updates a State object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        return abort(400, {'message': 'Not a JSON'})

    check = ["id", "state_id", "created_at", "updated_at"]

    for k, v in request.get_json().items():
        if k not in check:
            setattr(state, k, v)
    storage.save
    return jsonify(state.to_dict()), 200
