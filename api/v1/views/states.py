#!/usr/bin/python3
""" States view for API. """
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getallstate():
    """Gets all states"""
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())

    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getstate(state_id=None):
    """Gets a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletestate(state_id=None):
    """Deletes a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def createstate():
    """Creates a state"""
    state_req = request.get_json(silent=True)
    if state_req is None:
        abort(400, "Not a JSON")
    elif "name" not in state_req.keys():
        abort(400, "Missing name")
    else:
        new_state = state.State(**state_req)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict(), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updatestate(state_id=None):
    """Update a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    state_req = request.get_json(silent=True)
    if state_req is None:
        abort(400, "Not a JSON")
    else:
        for key, val in s.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, val)
        storage.save()
        return jsonify(state.to_dict(), 200)
