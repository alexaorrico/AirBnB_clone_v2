#!/usr/bin/python3
"""RESTful API for State"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def all_states():
    states = storage.all(State).values()

    if request.method == 'GET':
        new_list = []
        for state in states:
            new_list.append(state.to_dict())
        return jsonify(new_list)

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'name' not in request.json:
            abort(400, 'Missing name')
        obj = State(**request.get_json())
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['DELETE', 'GET', 'PUT'])
def one_state(state_id):
    states = storage.all(State).values()
    state = [state for state in states if state.id == state_id]
    if len(state) == 0:
        abort(404)

    if request.method == 'GET':
        return state[0].to_dict()

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for k, v in request.get_json().items():
            if k != 'id' and k != 'created_at' and k != 'updated_at':
                setattr(state[0], k, v)
        storage.save()
        return jsonify(state[0].to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(state[0])
        storage.save()
        return {}, 200
