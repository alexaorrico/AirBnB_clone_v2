#!/usr/bin/python3
"""VIew for States"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.state import State
from flask import abort
from flask import make_response
from flask import request


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_states():
    """Return all states"""
    dict_states = storage.all(State)
    states = []
    for state in dict_states.values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_states(state_id):
    """Return state according class and id of state
        or return Error: Not found if it doesn't exist.
    """
    if state_id:
        dict_state = storage.get(State, state_id)
        if dict_state is None:
            abort(404)
        else:
            return jsonify(dict_state.to_dict())


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Deletes an object State if exists, otherwise raise
        404 error
    """
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        else:
            storage.delete(state)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def response_state():
    """Post request that allow to create a new State if exists the name
        or raise Error if is not a valid json or if the name is missing
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()
    if "name" not in req:
        return make_response(jsonify({"error": "Missing name"}), 400)
    state = State(**req)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """Updates attributes from an State object"""
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)

        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
