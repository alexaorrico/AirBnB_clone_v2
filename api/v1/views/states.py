#!/usr/bin/python3
"""
Create a flask app that will serve the API, views module
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states',
                 methods=['GET'], strict_slashes=False)
def get_states():
    """
    Return states
    """
    states = storage.all(State)
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>',
                 methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Return state
    """
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Delete state
    """
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states',
                 methods=['POST'], strict_slashes=False)
def post_state():
    """
    Create state
    """
    if request.content_type != 'application/json':
        return abort(400, "Not a JSON")
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    if 'name' not in data:
        return abort(400, "Missing name")
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    Update state
    """
    if request.content_type != 'application/json':
        return abort(400, "Not a JSON")
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
