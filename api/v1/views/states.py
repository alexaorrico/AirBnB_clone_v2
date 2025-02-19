#!/usr/bin/python3
"""
Creates new view for State obj that handles all the restful API
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    states = storage.all(State).values()
    state_json = [state.to_dict() for state in states]
    return jsonify(state_json)


@app_views.route('states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_json = state.to_dict()
    return jsonify(state_json)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    if not request.get_json:
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
