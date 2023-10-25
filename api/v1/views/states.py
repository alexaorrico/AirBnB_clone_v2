#!/usr/bin/python3
"""api states"""
from flask import abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
import json


@app_views.route('/states', methods=['GET'])
def get_states():
    """retrieves all State object"""
    allStates = storage.all(State).values()
    statesList = []
    for state in allStates:
        statesList.append(state.to_dict())
    response = make_response(json.dumps(statesList), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/states/<id>', methods=['GET'])
def get_state(id):
    """retrieves State object with id"""
    state = storage.get(State, id)
    if not state:
        abort(404)
    response_data = state.to_dict()
    response = make_response(json.dumps(response_data), 200)
    response.headers['Content-Type'] = 'application/json'

    return response

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """delets state with id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    res = {}
    response = make_response(json.dumps(res), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
