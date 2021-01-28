#!/usr/bin/python3
"""
Module that handles the class State in API
"""

from models.state import State
from models import storage
import json
from flask import Flask, jsonify, request, make_response, abort
from api.v1.views import app_views


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def api_GET_dict(state_id=None):
    """Uses the models class to_dict to retreive all state objects"""
    states = storage.all("State")
    all_states = []

    if state_id is None or state_id is "":
        for state in states.values():
            all_states.append(state.to_dict())
        return jsonify(all_states)
    else:
        for state in states.values():
            if state.id == state_id:
                return jsonify(state.to_dict())
    abort(404)
    return


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def api_DEL_State(state_id):
    """Use models class to delete an instace of class State"""
    states = storage.all(State)

    for state in states.values():
        if state.id == state_id:
            state.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def api_POST_State():
    """Method to create a State"""
    payload = request.get_json(silent=True)

    if payload is None:
        abort(400, 'Not a JSON')
    elif 'name' not in payload:
        abort(400, 'Missing name')

    new_state = State(**payload)
    new_state.save()

    return(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def api_PUT_State(state_id):
    """Method to update a state object"""
    payload = request.get_json(silent=True)
    states = storage.all(State)

    if payload is None:
        abort(400, 'Not a JSON')

    for state in states.values():
        if state.id == state_id:
            for k, v in payload.items():
                if k != 'created_at' and k != 'updated_at' and k != 'id':
                    setattr(state, k, v)
            return(jsonify(state.to_dict()), 200)
    abort(404)
