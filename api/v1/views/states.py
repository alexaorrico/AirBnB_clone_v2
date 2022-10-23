#!/usr/bin/python3
""" A new view for State objects that handles
all default RESTFul API actions. """
from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getallstates():
    """ Retrieves the list of all State objects. """
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())

    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getstate(state_id=None):
    """ Retrieves a State object given its id. """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletestate(state_id=None):
    """ Deletes a state. """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def createstate():
    """ Creates a state. """
    state_req = request.get_json()
    if not state_req:
        abort(400, description="Not a JSON")

    if "name" not in state_req:
        abort(400, description="Missing name")

    new_state = State(**state_req)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updatestate(state_id=None):
    """Update a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    state_req = request.get_json()

    if not state_req:
        abort(400, description="Not a JSON")
    
    ignore_keys = ['id', 'created_at', 'updated_at']
    
    for key, val in state_req.items():
        if key not in ignore_keys:
            setattr(state, key, val)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
