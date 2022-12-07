#!/usr/bin/python3
"""Views for the State class: GET, DELETE,  POST, PUT"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    objs = []
    for x in storage.all(State).values():
        objs.append(x.to_dict())
    return jsonify(objs)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    obj = State(**request.get_json())
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state.__dict__.update(request.get_json())
    old_dict = state.to_dict()
    storage.delete(state)
    state = State(**old_dict)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 200
