#!/usr/bin/python3
"""
Module to create view for State objects handling default
RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route("/states/", methods=["GET"])
def state_get():
    """
    Retrieves list of all State objects.
    """
    all_states = storage.all(State)
    states_list = []
    for state in all_states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<string:state_id>", methods=["GET"])
def state_id_get(state_id):
    """
    Retrieves a state with a given id
    Raise 404 error if id not linked to any State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<string:state_id>", methods=["DELETE"])
def state_id_delete(state_id):
    """
    Deletes a State object with a given id
    Raise 404 error if id not linked to any State object
    Returns and empty dictionary with status code 200
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)



@app_views.route("/states/", methods=["POST"])
def state_post():
    """
    Creates a State via POST
    If the HTTP body request is not valid JSON, raise 400 error, Not a JSON
    If the dictionary doesn't contain the key name, raise a 400 error with
    message Missing name
    Returns new State with status code 201
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_state = State(**request.get_json())
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)



@app_views.route("/states/<string:state_id>", methods=["PUT"])
def state_put(state_id):
    """
    Updates a State object via PUT
    If the state_id is not linked to any State object, raise 404 error
    If the HTTP body request is not valid JSON, raise a 400 error, Not a JSON
    Update the State object with all key-value pairs of the dictionary
    Ignore keys: id, created_at, updated_at
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in request.get_json().items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
