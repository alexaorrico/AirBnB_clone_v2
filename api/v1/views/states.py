#!/usr/bin/python3
""" Handles Restful API actions for states """
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utols import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Returns list of all state objects"""
    allstates = storage.all(State).values()
    states_list = []
    for state in allstates:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Returns state matching ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes state with the given ID"""

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>', methods=['POST'], strict_slashes=False)
def put_state(state_id):
    """Creates a State Object"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    info = request.get_json()
    state_inst = State(**info)
    state_inst.save()
    return make_response(jsonify(state_inst.todict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Updates the state object"""
    state = Storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    titles_ignore = ['id', 'created_at', 'updated_at']

    state_info = request.get_json()
    for key, value in state_info.items():
        if key not in titles_ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
