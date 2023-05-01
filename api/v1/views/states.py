#!/usr/bin/python3
"""
A new view for state objects that handles all RESTFul api
"""
from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def all_states():
    """
    get the list list of all state objects
    """
    states = storage.all('State')
    s_list = []
    for state in states.values():
        s_list.append(state.to_dict())
    return jsonify(s_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_a_state(state_id):
    states = storage.all('State')
    for state in states.values():
        if state.id == state_id:
            state = state.to_dict()
            return jsonify(state)
    abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_a_state(state_id):
    """deletes a state objects"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_post():
    """
    Create an instance of the state object
    """
    if not request.get_json():
        return jsonify({"error": "Not a Json"})
    if "name" not in request.get_json():
        return jsonify({"error": "Mising name"}), 400

    js = request.get_json()
    state = State(**js)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put(state_id):
    """
    method to put into data into the state objects
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a Json"}), 400)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in request.get_json():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())
