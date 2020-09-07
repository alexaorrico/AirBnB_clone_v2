#!/bin/bash python3
""" state view """
from api.v1.views import app_views
from flask import jsonify, Blueprint, render_template, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=["GET"])
def get_all_states():
    """ retrieves all state objects """
    states = storage.all(State).values()
    json_states = states.to_dict()
    return json_states


@app_views.route('/states/<state_id>', methods=["GET"])
def get_a_state(state_id):
    """ retrieves one unique state object """
    state = [state for states in states if state['id'] == state_id]
    if len(state) == 0:
        return (jsonify({"error": "Not found"}))
    json_state = state.to_dict()
    return json_states


@app_views.route('/states/<state_id>', methods=["GET", "DELETE"])
def del_a_state(state_id):
    """ retrieve a state and delete it """
    state = [state for states in states if state['id'] == state_id]
