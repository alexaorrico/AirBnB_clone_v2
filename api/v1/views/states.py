#!/usr/bin/python3
"""Handles all default api actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from models.state import State
from flask import make_response


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Returns all states"""
    dic_states = storage.all(State)
    states = []
    for state in dic_states.values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def one_state(state_id):
    """Return state according to its id
    or return 404 error if it doesn't exist
    """
    if state_id:
        dic_state = storage.get(State, state_id)
        if dic_state is None:
            abort(404)
        else:
            return jsonify(dic_state.to_dict())


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Deletes an object State if exists, otherwise raise 404 errer"""
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        else:
            storage.delete(state)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a new state, otherwise raises error if it is not a valid json
    or the name is missing
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    reque = request.get_json()
    if "name" not in reque:
        return make_response(jsonify({"error": "Missing name"}), 400)
    state = State(**reque)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates attributes from an State object"""
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)

        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        reque = request.get_json()
        for key, value in reque.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
