#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """liste all state"""
    list_states = []
    all_states = storage.all(State).values()
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>',
                 methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """get one state"""
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """ Delete a state"""
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states',
                 methods=['POST'], strict_slashes=False)
def add_state():
    """add a state"""
    requeste = request.get_json()
    if requeste is None:
        abort(400, "Not a JSON")
    if 'name' not in requeste.keys():
        abort(400, "Missing name")
    new_state = State(**requeste)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """update a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    requeste = request.get_json()
    if requeste is None:
        abort(400, "Not a JSON")
    for key, value in requeste.items():
        setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
