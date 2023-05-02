#!/usr/bin/python3
"""View for State objects"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """returns list of all State objects in JSON"""
    states_obj = storage.all(State)
    states = []
    for state in states_obj:
        states.append(states_obj[state].to_dict())
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """return JSON of state with the id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """deletes a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def add_state():
    """ creates a new State"""
    req_json = request.get_json()
    if not req_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in req_json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_state = State(**req_json)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """updates a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req_json = request.get_json()
    if not req_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in req_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
