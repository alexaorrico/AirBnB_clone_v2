#!/usr/bin/python3
""" Handles all State requests for the API """

from api.v1.views import app_views
from flask import jsonify, make_response
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def all_states(state):
    """ Returns a JSON of all State objects """
    states = []
    for obj in storage.all(State).values():
        states.append(obj.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def one_state(state_id):
    """ Returns a JSON of a state whose id was requested """
    obj = storage.get(State, state_id)
    if obj is not None:
        return jsonify(obj.to_dict())
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes an obj whose id was passed """
    if storage.get(State, state_id) is None:
        return make_response(jsonify({"error": "Not found"}), 404)
