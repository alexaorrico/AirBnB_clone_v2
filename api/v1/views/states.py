#!/usr/bin/python3
"""
Router for handling API calls on State objects
"""
from os import abort
from api.v1.views import app_views
from flask import jsonify
from flask import request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """Get all states objects"""
    arrayOfStates = []
    for value in storage.all(State).values():
        arrayOfStates.append(value.to_dict())
    return jsonify(arrayOfStates), 200


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def oneState(state_id):
    """Get one state based on his id"""
    try:
        state = storage.get(State, state_id).to_dict()
        return jsonify(state), 200
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def deleteState(state_id):
    """Delete one state"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def createState():
    "Creates a state"
    if not request.is_json:
        return jsonify(error='Not a JSON'), 400

    body = request.get_json()
    name = body.get('name')
    if not name:
        return jsonify(error='Missing name'), 400

    newState = State(name=name)
    newState.save()
    return jsonify(newState.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updateState(state_id):
    """Update a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        if not request.is_json:
            return jsonify(error='Not a JSON'), 400

        body = request.get_json()
        if 'name' in body:
            state.name = body['name']
            state.save()
            return jsonify(state.to_dict()), 200

        return jsonify(error='Missing name'), 400
