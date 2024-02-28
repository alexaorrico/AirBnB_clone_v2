#!/usr/bin/python3
""" Handles all State requests for the API """

from api.v1.views import app_views
from flask import jsonify
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def all_states(state):
    """ Returns a JSON of all State objects """
    states = []
    for obj in storage.all(State).values():
        states.append(obj.to_dict())
    return jsonify(states)


@app_views.route('/states/<int: state_id>')
def one_state(state_id):
    """ Returns a JSON of a state whose id was requested """
    obj = storage.get(State, state_id)
    if obj is not None:
        return jsonify(obj.to_dict())
    return jsonify({"e"})
        
