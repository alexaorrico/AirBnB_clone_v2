#!/usr/bin/python3

"""Module to handle state request Blueprint"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """return json array of all states"""
    list_states = []
    states = storage.all(State).values()
    for state in states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new state"""
    if request.get_json():
        body = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in body:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_state = State(**body)
    new_state.save()
    if storage.get(State, new_state.id) is not None:
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Method to get a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """delete a single state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """update properties of a single state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.get_json():
        body = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    _exceptions = ["id", "created_at", "updated_at"]
    for k, v in body.items():
        if k not in _exceptions:
            setattr(state, k, v)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
