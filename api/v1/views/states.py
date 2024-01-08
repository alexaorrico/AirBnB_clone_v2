#!/usr/bin/python3
"""
Module for state api
"""
from flask import Flask, jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route("/states", strict_slashes=False, methods=['GET'])
@app_views.route("/states/<state_id>", strict_slashes=False, methods=['GET'])
def get_state_objs(state_id=None):
    """returning all states or sing state"""
    if state_id is None:
        states = storage.all(State).values()
        return jsonify([state.to_dict() for state in states])
    else:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        else:
            return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_obj(state_id):
    """deletes an object based on id given"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def post_state():
    """Creating a new state"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """updating specific state using id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict()), 200
