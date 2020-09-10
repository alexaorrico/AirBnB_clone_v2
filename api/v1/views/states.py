#!/usr/bin/python3
"""States views"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def states_get():
    """Retrieves the list of all State objects"""
    states = []
    for state in storage.all('State').values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_states(state_id):
    """Retrieves the list of all State objects"""
    key_id = 'State.' + state_id
    states = storage.all('State')
    if key_id in states:
        return jsonify(states[key_id].to_dict())
    else:
        abort(404)


@app_views.route('/states/<string:state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    if state_id:
        states = storage.get(State, state_id)
        if states is None:
            abort(404)
        states.delete()
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """Creates a State"""
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    elif "name" not in req:
        abort(400, "Missing name")
    new = State(**req)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """Update a State object"""
    req = request.get_json()
    if state_id:
        states = storage.get(State, state_id)
        if states is None:
            abort(404)
        if req is None:
            abort(400, "Not a JSON")
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(states, key, value)
        storage.save()
        return jsonify(states.to_dict()), 200
