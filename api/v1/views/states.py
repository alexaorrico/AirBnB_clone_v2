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


@app_views.route('/states', methods=['POST'])
def create_state():
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    storage.new(State(**request.get_json()))
    storage.save()
    return jsonify(State(**request.get_json().to_dict())), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    if not request.get_json():
        abort(400, 'Not a JSON')
    if storage.get(State, state_id) is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in {'id', 'created_at', 'updated_at'}:
            setattr(request.get_json(), k, v)
    storage.save()
    return jsonify(storage.get(State, state_id).to_dict()), 200
