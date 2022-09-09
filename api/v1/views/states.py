#!/usr/bin/python3
"""
State
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """
    Retrieves the list of all State objects
    """
    states = storage.all("State")
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return(jsonify(states_list))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id(state_id):
    """
    Retrieves a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return (jsonify(state.to_dict()))


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a State
    """
    if not request.get_json():
        error = {"error": "Not a JSON"}
        return (jsonify(error), 400)
    if "name" not in request.get_json():
        no_name = {"error": "Missing name"}
        return (jsonify(no_name), 400)
    obj_dict = request.get_json()
    state = State(**obj_dict)
    state.save()
    return (jsonify(state.to_dict()), 201)

@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        error = {"error": "Not a JSON"}
        return (jsonify(error), 400)
    obj_dict = request.get_json()
    state.name = obj_dict["name"]
    state.save()
    return (jsonify(state.to_dict()), 200)
