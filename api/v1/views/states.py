#!/usr/bin/python3
"""Module contains a view for state objects"""

from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify
from flask import abort
from flask import request
from flask import make_response


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getStates():
    """Fetch a list of all states"""
    statesList = []
    statesData = storage.all(State).values()
    for state in statesData:
        statesList.append(state.to_dict())
    return jsonify(statesList)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getStateId(state_id):
    """Fetch a specific state using state_id given"""
    allStates = storage.all(State).values()
    for state in allStates:
        stateDict = state.to_dict()
        if state_id == stateDict['id']:
            return jsonify(stateDict)
    abort(404)


@app_views.route(
    '/states/<state_id>', methods=['DELETE'], strict_slashes=False
)
def deleteState(state_id):
    """Deletes the state whose id is given"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def createState():
    """Creating a state"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    userData = request.get_json()
    newState = State(**userData)
    newState.save()

    return make_response(jsonify(newState.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updateState(state_id):
    """Update a specific state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    userData = request.get_json()
    for k, v in userData.items():
        if k not in ['created_at', 'updated_at', 'id']:
            setattr(state, k, v)
    storage.save()

    return make_response(jsonify(state.to_dict()), 200)
