#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=['GET'])
@app_views.route("/states/<state_id>", methods=['GET'])
def retrieve_state(state_id=None):
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            return make_response(jsonify({"error": "Not found"}), 404)
        return jsonify(state.to_dict())
    states = storage.all(State)
    states = [state.to_dict() for state in states.values()]
    return jsonify(states)
