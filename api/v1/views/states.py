#!/usr/bin/python3
"""
Flask route that returns states as json

Hnadle GET, POST, PUT, DELETE action
"""

from flask import jsonify, request, render_template, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states():
    """Retrives all objects"""
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route("/states/<string:state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """get state information for specified state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route("/states/<string:state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """get state information for specified state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})
    # set status code 200 in return expression
