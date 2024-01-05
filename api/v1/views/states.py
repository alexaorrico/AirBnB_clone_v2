#!/usr/bin/python3
"""API Routes for State Model"""
from werkzeug.exceptions import BadRequest

from models import storage
from api.v1.views import app_views
from models.state import State
from flask import abort, request, jsonify


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state_view(state_id=None):
    """states endpoint: GET, POST, UPDATE, DELETE"""
    if request.method == 'GET' and not state_id:
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
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        return state.to_dict()
    elif request.method == 'DELETE':
        storage.delete(state)
        return {}, 200
    elif request.method == 'PUT':
        try:
            special_keys = ['id', 'created_at', 'updated_at', '__class__']
            data = request.get_json()
            for k, v in data.items():
                if k not in special_keys:
                    setattr(state, k, v)
            state.save()
            return state.to_dict(), 200
        except BadRequest:
            return jsonify({"error": "Not a JSON"}), 400
