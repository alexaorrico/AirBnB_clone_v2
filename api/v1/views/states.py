#!/usr/bin/python3
"""
The function is to retrieve all JSON versions
of states and convert them to the to_dict method
"""
from models.state import State
from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views


@app_views.route('/api/v1/states', methods=['GET'])
def get_states():
    states = storage.all(State)
    states_list = [state.to_dict() for state in states]
    return jsonify(states_list)


"""@app_views.route('/api/v1/states', methods=['GET'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())"""


@app_views.route('api/v1/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def get_delete_update_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state)
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200


@app_views.route('api/v1/states', methods=['POST'])
def create_state():
    data = request.get_json()
    if 'state_id' not in State:
        abort(404)
    # If the request isn't valid JSON or
    # doesn't contain the name, raise a 400 error
    if data is None:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")

    # Create a new State
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201
