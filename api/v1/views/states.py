#!/usr/bin/python3
"""
State
"""

from api.v1.app import not_found
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    states = storage.all("State")
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return(jsonify(states_list))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id(state_id):
    state = storage.get(State, state_id)
    if state is None:
        not_found(404)
    return (jsonify(state.to_dict()))


@app_views.route('/states/<state_id>', methods=['DELETE'],
    strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        not_found(404)
    state.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    if not request.get_json():
        error = {"error": "Not a JSON"}
        return (jsonify(error), 400)
    elif "name" not in request.get_json():
        no_name = {"error": "Missing name"}
        return (jsonify(no_name), 400)
    else:
        obj_dict = request.get_json()
        obj = State(obj_dict)
        obj.save()
        return (jsonify(obj.to_dict()), 201)
