#!/usr/bin/python3
""" Handles all State requests for the API """

from api.v1.views import app_views
from flask import jsonify, make_response, request
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
    obj = storage.get(State, state_id)
    if obj is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(obj)
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'])
def add_state(state):
    """ Creates a new state obj into the db """
    try:
        new = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)
    if 'name' not in new.keys():
        return make_response("Missing name", 400)
    obj = State(**new)
    obj.save()
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ Updates a state obj with the dict from HTTP request """
    obj = storage.get(State, state_id)
    if obj is None:
        return 
    try:
        new = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)
    
