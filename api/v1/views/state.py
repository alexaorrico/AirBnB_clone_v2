#!/usr/bin/python3
"""State obj API"""
from flask import Flask, jsonify, abort
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    if state_id is None:
        states = storage.all(State)
        return jsonify(states)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())
