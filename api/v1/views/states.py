#!/usr/bin/python3
""" retruns json response status of API """
from flask import Flask, abort, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    ''' gets list of all state objects '''
    states_list = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    return jsonify(state_object.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delte_state(state_id):
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}))
