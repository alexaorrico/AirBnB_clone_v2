#!/usr/bin/python3

""" Routes States"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, state

def validate_state(state_id):
    """ Validate if state with given ID exists """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)  # Raise a 404 error if state is not found
    return state

@app_views.route('/states/', methods=['GET', 'POST'], strict_slashes=False)
def handle_states():
    if request.method == 'GET':
        states = storage.all(State).values()
        return jsonify([state.to_dict() for state in states])

    if request.method == 'POST':
        data = request.get_json()
        if not data or 'name' not in data:
            abort(400)  # Bad request if data is missing or name is not provided
        new_state = State(**data)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201  # 201 Created status

@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def handle_state(state_id):
    state = validate_state(state_id)

    if request.method == 'GET':
        return jsonify(state.to_dict())

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400)  # Bad request if data is missing
        for key, value in data.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict())

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200  # Empty response with 200 OK status