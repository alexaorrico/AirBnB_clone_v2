#!/usr/bin/python3
""" Handle state API"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """retrive all states object"""
    allStates = storage.all(State).values()
    statesList = []
    for state in allStates:
        statesList.append(state.to_dict())
    return jsonify(statesList)


@app_views.route('/states/<id>', methods=['GET'], strict_slashes=False)
def get_state(id):
    """retrive state object with a particular id"""
    state = storage.get(State, id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<id>', methods=['DELETE'], strict_slashes=False)
def del_state(id):
    """Delete a state object"""
    state = storage.get(State, id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    res = request.get_json()
    if type(res) != dict:
        abort(400, "Not a JSON")
    if "name" not in res:
        abort(400, "Missing name")
    state = State(**res)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<id>', methods=['PUT'], strict_slashes=False)
def update_state(id):
    state = storage.get(State, id)
    if not state:
        abort(404)
    res = request.get_json()
    if not res:
        abort(400, "Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    for item in res:
        if item not in ignore:
            setattr(state, item, res[item])
    storage.save()
    return jsonify(state.to_dict()), 200
