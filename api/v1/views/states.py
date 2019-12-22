#!/usr/bin/python3
"""
Views for State
"""
from flask import request, abort, jsonify
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """
    Retrieves the list of all State objects: GET /api/v1/states
    Creates a State: POST /api/v1/states
    """
    if request.method == 'GET':
        list_states = []
        states = storage.all('State').values()
        for state in states:
            list_states.append(state.to_dict())
        return jsonify(list_states), 200

    if request.method == 'POST':
        request_json = request.get_json()
        if request_json:
            return jsonify(error='Not a JSON'), 400
        if 'name' not in request_json:
            return jsonify(error='Missing name'), 400
        state = State(**request_json)
        storage.new(state)
        storage.save()
        return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def state(state_id=None):
    """
    Retrieves the list of all State objects: GET /api/v1/states
    Creates a State: POST /api/v1/states
    """
    if request.method == 'GET':
        state = storage.get('State', state_id)
        if state:
            return jsonify(state.to_dict()), 200
        abort(404)

    if request.method == 'DELETE':
        state = storage.get('State', state_id)
        if state:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
        abort(404)

    if request.method == 'PUT':
        request_json = request.get_json()
        if not isinstance(request_json, dict):
            return jsonify(error='Not a JSON'), 400
        state = storage.get('State', state_id)
        if state:
            for key, value in request_json.items():
                if key not in ["__class__", "id", "created_at", "updated_at"]:
                    setattr(state, key, value)
            storage.save()
            return jsonify(state.to_dict()), 200
        abort(404)
