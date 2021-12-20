#!/usr/bin/python3
''' Creating states flask app '''


from flask import Flask, jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import app_views
import json


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def allStates():
    ''' returns all states '''

    allState = storage.all(State)
    stateList = []

    for value in allState.values():
        stateList.append(value.to_dict())

    return jsonify(stateList)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getStateID(state_id):
    ''' Gets the state id'''

    stateID = storage.get(State, state_id)

    if stateID is None:
        abort(404)

    return jsonify(stateID.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteState(state_id):
    ''' Deleting a state matching id'''

    focusedState = storage.get(State, state_id)

    if focusedState is None:
        abort(404)

    storage.delete(focusedState)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def postState():
    ''' creates a new state '''

    if not request.is_json:
        abort(400, description='Not a JSON')

    jsonReq = request.get_json()

    if 'name' not in jsonReq:
        abort(400, description='Missing name')

    newState = State(**jsonReq)

    storage.new(newState)
    storage.save()

    return jsonify(newState.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updateState(state_id):
    ''' updates a state object '''

    focusedState = storage.get(State, state_id)

    if focusedState is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    jsonReq = request.get_json()
    ignoreKeys = ['id', 'created_at', 'updated_at']

    for key, value in jsonReq.items():
        if key not in ignoreKeys:
            setattr(focusedState, key, value)

    storage.save()

    return jsonify(focusedState.to_dict()), 200
