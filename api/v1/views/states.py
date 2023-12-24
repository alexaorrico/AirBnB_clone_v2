#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API actions"""
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request


@app_views.route('/states', methods=['GET'])
def all_states():
    all_states = []
    for state in storage.all(State).values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_obj(state_id):
    if storage.get(State, state_id) is None:
        abort(404)
    return jsonify(storage.get(State, state_id).to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    if storage.get(State, state_id) is None:
        abort(404)
    storage.delete(storage.get(State, state_id))
    storage.save()
    return {}, 200


@app_views.route('/states/', methods=['POST'])
def create_state():
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):

    existing_state = storage.get(State, state_id)
    if existing_state is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for k, v in data.items():
        if k not in {'id', 'created_at', 'updated_at'}:
            setattr(existing_state, k, v)
    storage.save()
    return jsonify(existing_state.to_dict()), 200
