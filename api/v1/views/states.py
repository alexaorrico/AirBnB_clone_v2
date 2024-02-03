#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, jsonify, request
import json


@app_views.route('/states', methods=['GET'])
def all_states():
    states_dict = storage.all(State)
    states_list = [state.to_dict() for state in states_dict.values()]
    return states_list


@app_views.route('/states/<state_id>', methods=['GET'])
def states_id(state_id):
    state = storage.get(State, state_id)
    if state:
        return state.to_dict(), 201
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def states_delete(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify('{}'), 201


@app_views.route('/states', methods=['POST'])
def states_post():
    try:
        data = request.get_data()
        data_object = json.loads(data.decode('utf-8'))
        if 'name' not in data_object:
            abort(400, 'Missing name')
        new_state = State(**data_object)
        storage.new(new_state)
        storage.save()
    except json.JSONDecodeError:
        abort(400, 'Not a JSON')
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def states_put(state_id):
    try:
        state_up = storage.get(State, state_id)
        if not state_up:
            abort(404)
        data = request.get_data()
        data_object = json.loads(data.decode('utf-8'))
        for key, value in data_object.items():
            setattr(state_up, key, value)
        storage.save()
    except json.JSONDecodeError:
        abort(400, 'Not a JSON')
    return jsonify(state_up.to_dict()), 201
