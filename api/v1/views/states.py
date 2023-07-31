#!/usr/bin/env python3
"""
This script creates a new view for State objects that handles all default RESTFul API actions:

In the file api/v1/views/states.py
You must use to_dict() to retrieve an object into a valid JSON
Update api/v1/views/__init__.py to import this new file
"""
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """retrieve the list of all states or post new one"""
    if request.method == 'GET':
        states = storage.all(State)
        state_list = []
        for state in states.values():
            state_list.append(state.to_dict())
            return jsonify(state_list)
    elif request.method == 'POST':
        data = request.get_json()
        if type(data) is not dict:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if data.get('name') is None:
            return make_response(jsonify({"error": "Missing name"}), 400)
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201
    abort(404)


@app_views.route('/states/<string:state_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def alt_states(state_id):
    """alter the values of state"""
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state_id not in state.keys():
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if type(data) is not dict:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        for k, v in data.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(state, k, v)
                storage.save()
        return jsonify(state.to_dict()), 201
