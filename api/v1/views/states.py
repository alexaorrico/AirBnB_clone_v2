#!/usr/bin/python3
"""
new view for State objects that handles all default RESTFul API actions
"""

import json
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import request
from flask import abort
from flask.json import jsonify


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """
    Retrieves the list of all State objects
    """
    if state_id is None:
        info = []
        for state in storage.all(State).values():
            info.append(state.to_dict())
        return jsonify(info)
    for state in storage.all(State).values():
        if state.id == state_id:
            return jsonify(state.to_dict())

    abort(404)


@app_views.route('states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """
    deletes state
    """
    for state in storage.all(State).values():
        if state.id == state_id:
            state.delete()
            storage.save()
            return jsonify({}), 200

    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """
    creates a state
    """
    json = request.get_json(silent=True)
    if json is None:
        abort(400, 'Not a JSON')
    if 'name' not in json:
        abort(400, 'Missing name')
    new = State(**json)
    new.save()

    return jsonify(new.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """
    updates a state
    """
    for state in storage.all(State).values():
        if state.id == state_id:
            json = request.get_json(silent=True)
            if json is None:
                abort(400, 'Not a JSON')
            for key, value in json.items():
                if key != 'updated_at' and key != 'created_at' and key != 'id':
                    setattr(state, key, value)
            state.save()
            return jsonify(state.to_dict()), 200
    abort(404)
