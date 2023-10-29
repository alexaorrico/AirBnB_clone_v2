#!/usr/bin/python3
""" states.py that handles all default RestFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, request, jsonify


@app_views.route("/states", strict_slashes=False)
def all_states():
    """ all states"""
    len = storage.count(State)
    new_list = []
    for i in range(len):
        state = State.to_dict(list(storage.all(State).values())[i])
        new_list.append(state)
    print(new_list)
    return new_list


@app_views.route("/states/<string:state_id>", strict_slashes=False)
def get_state(state_id):
    """ get state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return State.to_dict(state)


@app_views.route("/states/<string:state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ delete state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return {}, 200


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def post_state():
    """ post state"""

    request_data = request.get_json()
    if not request_data:
        return jsonify({'message': 'Not a JSON'}), 400
    if 'name' not in request_data:
        return jsonify({'message': 'Missing name'}), 400

    new_state = State()
    new_state.name = request_data['name']
    storage.new(new_state)
    storage.save()

    return State.to_dict(new_state), 201


@app_views.route("/states/<string:state_id>", methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """ put state"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        return jsonify({'message': 'Not a JSON'}), 400
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return State.to_dict(state), 200
