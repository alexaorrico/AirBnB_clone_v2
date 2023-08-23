#!/usr/bin/python3
"""States Module
"""
from api.v1 import app
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.state import State


@app.route('/api/v1/states', methods=['GET'])
def get_states():
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app.route('/api/v1/states/<state_id>', methods=['GET'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app.route('/api/v1/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app.route('/api/v1/states', methods=['POST'])
def create_state():
    data = request.get_json()
    if not data:
        return jsonify(error="Not a JSON"), 400
    if "name" not in data:
        return jsonify(error="Missing name"), 400

    state = State(name=data['name'])
    state.save()
    return jsonify(state.to_dict()), 201


@app.route('/api/v1/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify(error="Not a JSON"), 400

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()

    return jsonify(state.to_dict()), 200
