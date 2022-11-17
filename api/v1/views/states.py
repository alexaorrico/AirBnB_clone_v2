#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import request, abort, jsonify
from models.state import State
from models import storage


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def statesWithId(state_id=None):
    """Methods that retrieves all methods for states with id"""
    stateId = storage.get(State, state_id)
    if request.method == 'GET':
        if stateId is None:
            return abort(404)
        return jsonify(stateId.to_dict())

    if request.method == 'DELETE':
        if stateId is None:
            return abort(404)
        stateId.delete()
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        if stateId is None:
            return abort(404)
        if request.get_json() is None:
            return abort(400, 'Not a JSON')
        toIgnore = ["id", "created_at", "updated_it"]
        for key, value in request.get_json().items():
            if value not in toIgnore:
                setattr(stateId, key, value)
        stateId.save()
        return jsonify(stateId.to_dict()), 200


@app_views.route('/states', methods=['POST', 'GET'], strict_slashes=False)
def statesNoId():
    """Methods that retrieves all methods for states without id"""
    if request.method == 'POST':
        if request.get_json() is None:
            return abort(400, 'Not a JSON')
        if request.get_json().get('name') is None:
            return abort(400, 'Missing name')
        newState = State(**request.get_json())
        newState.save()
        return jsonify(newState.to_dict()), 201

    if request.method == 'GET':
        allState = storage.all(State)
        state = list(allObject.to_dict() for allObject in allState.values())
        return jsonify(state)
