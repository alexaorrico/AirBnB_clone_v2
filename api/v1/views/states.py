#!/usr/bin/python3
"""
states.py
"""
from . import app_views
from flask import Flask, jsonify
from models import storage
from models.state import State
from flask import abort
from flask import request


@app_views.route('/states', methods=['GET'])
@app_views.route('/states/', methods=['GET'])
def allstates():
    """
    Retrieves the list of all State objects
    """
    dict_of_states = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(dict_of_states)


@app_views.route('/states/<string:state_id>', methods=['GET'])
def state_by_id(state_id):
    """
    Retrieves a State object:
    GET /api/v1/states/<state_id>
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def delete_by_id(state_id):
    """
    Deletes a State object::
    DELETE /api/v1/states/<state_id>
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/', methods=['POST'])
@app_views.route('/states', methods=['POST'])
def create_state():
    """
    Creates a new State object
    """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')

    new_state = State(**data)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'])
def update_state(state_id):
    """
    updates a new State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignored_keys = ['id', 'updated_at', 'created_at']
    for key, value in data.items():
        if key in ignored_keys:
            continue
        setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
