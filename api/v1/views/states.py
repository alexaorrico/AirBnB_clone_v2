#!/usr/bin/python3
""" view for State """
from api.v1.views import app_views
from flask import jsonify, abort
from models.state import State
from models import storage
from flask import request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """ function to retrieve all states """
    if not state_id:
        states = storage.all(State)
        list_states = []
        for state in states.values():
            list_states.append(state.to_dict())
        return jsonify(list_states)
    else:
        state = storage.get(State, state_id)
        if state is None:
            return abort(404)
        return state.to_dict()


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(state_id):
    """ deletes state object """
    if state_id is None:
        return abort(404)
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ function to post a state """
    if not request.json or 'name' not in request.json:
        return 'Missing name', 400
    body = request.get_json()
    new_state = State(**body)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ function to use PUT API """
    if state_id is None:
        return abort(404)
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    if not request.json:
        return 'Not a JSON', 400
    body = request.get_json()
    for key, value in body.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            continue
        setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
