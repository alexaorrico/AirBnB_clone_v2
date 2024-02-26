#!/usr/bin/python3
"""
states.py
"""
from . import app_views
from flask import jsonify
from models import storage
from models.state import State
from flask import abort, request, Response, make_response
import json


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def allstates():
    """
    Retrieves the list of all State objects
    """
    dict_of_states = [obj.to_dict() for obj in storage.all(State).values()]
    response = Response(
        response=json.dumps(dict_of_states, indent=4),
        status=200,
        mimetype='application/json'
    )
    return response


@app_views.route('/states/<state_id>',
                 methods=['GET'], strict_slashes=False)
def state_by_id(state_id):
    """
    Retrieves a State object:
    GET /api/v1/states/<state_id>
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_by_id(state_id):
    """
    Deletes a State object::
    DELETE /api/v1/states/<state_id>
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a new State object
    """
    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json(force=True)
    if 'name' not in data:
        abort(400, 'Missing name')

    new_state = State(**data)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    updates a new State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json(force=True)
    ignored_keys = ['id', 'updated_at', 'created_at']
    for key, value in data.items():
        if key in ignored_keys:
            continue
        setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
