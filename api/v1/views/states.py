#!/usr/bin/python3

"""
a new view for State objects that handles all default RESTFul API actions
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def retrieve_state():
    """
    Retrieves all the states
    """

    state_list = []
    states = storage.all(State)
    for state in states.values():
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=["GET"],
                 strict_slashes=False)
def retrieve_state_using_stateid(state_id):
    """
    REtrieves the state using the state id
    Raises a 404 error if the state_id isnt linked to a state
    """

    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state_using_stateid(state_id):
    """
    Deletes a state using the state id
    Raises a 404 error If the state_id is not linked to any State object
    Returns an empty dictionary with the status code 200
    """

    state = storage.get(State, state_id)
    if state:
        state.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_state():
    """
    Posts a new city
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    state_data = request.get_json()
    state = State()
    for key, value in state_data.items():
        setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id):
    """
    Updates a state using the state id
    Returns a 404 error if the state id is not linked to any state
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    state = storage.get(State, state_id)
    keys_ignore = ["id", "updated_at", "created_at"]
    if state:
        for key, value in request.get_json().items():
            if key not in keys_ignore:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
    abort(404)
