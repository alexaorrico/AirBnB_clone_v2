#!/usr/bin/python3

"""Module to handle state request Blueprint"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, storage_t
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """return json array of all states"""
    if request.method == 'GET':
        states = storage.all(State).values()
        return jsonify([val.to_dict() for val in states])
    if request.method == 'POST':
        if request.get_json():
            body = request.get_json()
        else:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "name" not in body:
            return make_response(jsonify({"error": "Missing name"}), 400)

        new_state = State(**body)
        new_state.save()
        if storage.get(State, new_state.id) is not None:
            return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_state(state_id):
    """Method to get, delete or modify a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({})
    if request.method == 'PUT':
        if request.get_json():
            body = request.get_json()
        else:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        _exceptions = ["id", "created_at", "updated_at"]
        for k, v in body.items():
            if k not in _exceptions:
                setattr(state, k, v)
                # state[k] = v
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
