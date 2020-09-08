#!/bin/bash python3
""" state view """
from api.v1.views import app_views
from flask import jsonify, Blueprint, render_template, abort
from models import storage
from models.state import State
from models.base_model import BaseModel


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def get_all_states():
    """ retrieves all state objects """
    output = []
    states = storage.all(State).values()
    for state in states:
        output.append(state.to_dict())
    return (jsonify(output))


@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def get_a_state(state_id):
    """ retrieves one unique state object """
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            output = state.to_dict()
            return (jsonify(output))
    return jsonify({"error": "Not found"}), 404


@app_views.route('/states/<state_id>', methods=["GET", "DELETE"], strict_slashes=False)
def del_a_state(state_id):
    """ delete one unique state object """
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(state)
    storage.save()
    result = make_response(jsonify({}), 200)
    return result
