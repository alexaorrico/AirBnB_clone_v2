#!/usr/bin/python3
"""State obj API"""
from flask import Flask, jsonify, abort, make_response
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    if state_id is None:
        states = storage.all(State).values()
        states_list = [ state.to_dict() for state in states ]
        return jsonify(states_list)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state(state_id=None):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

@app_views.route('/states/<state_id>', methods=['POST'], strict_slashes=False)
