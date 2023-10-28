#!/usr/bin/python3
"""states.py"""
from models import storage
from flask import jsonify
from flask import Flask
from flask import request
from flask import abort
from api.v1.views import app_views
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieve all State objects"""
    states = storage.all("State").values()
    states_list = []
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>")
def get_state(state_id):
    """Retrieves a State by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_states(state_id):
    """Deletes a state ob by its id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return ({}, 200)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def post_state():
    """Posts data into db"""
    data = request.get_json()
    if not data:
        return jsonify({"message": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"message": "Missing name"}), 400
    state = State(name=data["name"])
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'])
def put_states(state_id):
    """Updates a State object using id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    to_be_ignored = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in to_be_ignored:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
