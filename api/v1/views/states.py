#!/usr/bin/python3
""" TBD """

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states', methods=["GET"])
def states():
    """retrieves list of all State objects"""
    states_dict = storage.all(State)
    states_list = []
    for value in states_dict.values():
        states_list.append(value.to_dict())
    return(jsonify(states_list))


@app_views.route('/states/<state_id>', methods=["GET"])
def states_id(state_id):
    """retrieves a state object"""
    res = storage.get(State, state_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/states/<state_id>', methods=["DELETE"])
def state_delete(state_id):
    """deletes a state object"""
    res = storage.get(State, state_id)
    if res is None:
        abort(404)
    storage.delete(res)
    return jsonify({}), 200

@app_views.route('/states', methods=["POST"])
def state_post():
    """creates a state object"""
    request_data = request.get_json()
    if request_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "name" not in request_data.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    stateobj = State(**request_data)
    storage.new(stateobj)
    statedict = stateobj.to_dict()
    return jsonify(statedict), 200
