#!/usr/bin/python3
from flask import Flask, jsonify, abort, request
from models.state import State
from api.v1.views import app_views

@app_views.route('/api/v1/states', methods=['GET'], strict_slashes=False)
def  all_State():
    """Retrieves the list of all State objects"""
    states = storage.all(state).value()
    for s in states:
        return jsonify([s.to_dict()])

@app_views.route('/api/v1/states/<state_id>', methods=['GET'], strict_slashes=False)
def inp_id(state_id):
    """Retrieves a State object:"""
     state = storage.get(State, state_id)

     if state is None:
         abort(404)
    return jsonify(state.to_dict())

@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def dellel(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return ({}), 200

@app_views.route('/api/v1/states', methods=['POST'], strict_slashes=False)
def postt():
    """Creates a State:"""
    dictt = request.get_json()

    if not dictt:
        abort(404, "Not a JSON")
    if "name" not in dictt:
        abort(404, "Missing name")
    State2 = State(**dictt)
    State2.save()
    return jsonify(state2), 201

@app_views.route('/api/v1/states/<state_id>', methods=['PUT'], strict_slashes=False)
def putt(state_id):
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    dictt = request.get_json()

    if not dictt:
        abort(404, "Not a JSON")
    for key, value in dictt.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
