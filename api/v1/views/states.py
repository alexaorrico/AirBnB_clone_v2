#!/usr/bin/python3
"""
Creating a new view for State objects that handles all default RESTFul API actions:
"""
from models import storage
from models.state import State

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    all_states = []
    states = storage.all(State).values()
    for state in states:
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<string:state_id>',
                 methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieve state object"""
    all_states = []
    states = storage.all("State").values()
    for state in states:
        all_states.append(state.to_dict())
    for a in all_states:
        if a.get("id") == state_id:
            return jsonify(a)
    abort(404)


@app_views.route('/states/<string:state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """deletes state object"""
    states = storage.all(State)
    try:
        k = 'State.' + state_id
        storage.delete(states[k])
        storage.save()
        return jsonify({}), 200
    except BaseException:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """creates a new state"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    else:
        request_body = request.get_json()

    if 'name' not in request_body:
        abort(400, "Missing name")
    else:
        state = State(**request_body)
        storage.new(state)
        storage.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:state_id>',
                 methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """updates state"""
    states = storage.all(State)
    try:
        k = 'State.' + state_id
        state = states[k]
        if not request.is_json:
            abort(400, 'Not a JSON')
        else:
            request_body = request.get_json()

        for k, v in request_body.items():
            if k != 'id' and k != 'created_at' and k != 'updated_at':
                setattr(state, k, v)
        storage.save
        return jsonify(state.to_dict()), 200

    except KeyError:
        abort(404)

    abort(501)
