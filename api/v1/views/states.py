#!/usr/bin/python3
"""API Routes for State Model"""
from werkzeug.exceptions import BadRequest

from models import storage
from api.v1.views import app_views
from models.state import State
from flask import abort, request, jsonify


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def state_list_view():
    """GET states or create a new state"""
    if request.method == 'GET':
        return [state.to_dict() for state in storage.all(State).values()]
    elif request.method == 'POST':
        try:
            data = request.get_json()
            if 'name' not in data:
                return jsonify({"error": "Missing name"}), 400
            state = State(**data)
            state.save()
            return state.to_dict(), 201
        except BadRequest:
            return jsonify({"error": "Not a JSON"}), 400


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state_detail_view(state_id):
    """GET, UPDATE or DELETE a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        return state.to_dict()
    elif request.method == 'DELETE':
        storage.delete(state)
        return {}
    elif request.method == 'PUT':
        try:
            special_keys = ['id', 'created_at', 'updated_at']
            prev_data = state.to_dict()
            data = {k: v for k, v in request.get_json() if k not in special_keys}
            new_data = prev_data.update(data)
            updated_state = State(new_data)
            return updated_state.to_dict(), 200
        except BadRequest:
            return jsonify({"error": "Not a JSON"}), 400
