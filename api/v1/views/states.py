#!/usr/bin/python3
""" states module """

from api.v1.views import app_views
from api import State
from api import storage
from flask import abort, jsonify, make_response, request


@app_views.route('/states', strict_slashes=False)
def allStates():
    """Retrives the list of all States objects"""
    allState = storage.all(State).values()
    listStates = []
    for state in all_states:
        listStates.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>',
                 methods=['GET', 'POST', 'PUT', 'DELETE'],
                 strict_slashes=False)
def stateById(state_id):
    """Retrieve, delete. create and update State"""       
    print(state_id)
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
