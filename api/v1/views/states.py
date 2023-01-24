#!/usr/bin/python3
"""
Flask route that returns json status response for State Objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def list_or_create_states():
    """
    function to get states or add state to storage
    """
    if request.method == 'GET':
        states = storage.all(State)
        return jsonify(
            [state.to_dict() for state in states.values()]
        )
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if data.get("name") is None:
            abort(400, "Missing name")
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_or_delete_or_update_state(state_id):
    """
    funtion to retrieve, delete or update particular state
    with state_id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(
            state.to_dict()
        )
    if request.method == 'DELETE':
        state.delete()
        del state
        return jsonify({}), 200
    if request.method == 'PUT':
        update = request.get_json()
        if update is None:
            abort(400, 'Not a JSON')
        for key, val in update.items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(state, key, val)
        state.save()
        return jsonify(state.to_dict()), 200
