#!/usr/bin/python3
"""creates a new view fro State that handles all Rest Api actions"""
from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def get_state(state_id=None):
    """retrieves the list of all state objects"""
    states = storage.all(State)
    if not state_id:
        # uses the '/states/ routes
        if request.method == 'GET':
            state_list = []
            for state in states.values():
                state_list.append(state.to_dict())
            return jsonify(state_list)
        elif request.method == 'POST':
            data = request.get_json()
            if not data:
                abort(400, 'Not a JSON')
            if not data.get('name'):
                abort(400, 'Missing name')
            new_obj = State(**data)
            new_obj.save()
            return jsonify(new_obj.to_dict()), 201
    else:
        # uses the '/states/<state_id>' route
        if request.method == 'GET':
            state = storage.get(State, state_id)
            if not state:
                abort(404)
            return jsonify(state.to_dict())
        elif request.method == 'DELETE':
            state_obj = storage.get(State, state_id)
            if not state_obj:
                abort(404)
            storage.delete(state_obj)
            storage.save()
            return jsonify({}), 200
        elif request.method == 'PUT':
            state_obj = storage.get(State, state_id)
            ignore_keys = ["id", "created_at", "updated_at"]
            if not state_obj:
                abort(404)
            data = request.get_json()
            if not data:
                abort(400, 'Not a JSON')
            state_obj.name = data.get('name')
            state_obj.save()
            return jsonify(state_obj.to_dict()), 200
