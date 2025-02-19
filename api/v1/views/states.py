#!/usr/bin/python3
""" API endpoints for states """

from models import storage
from models.state import State

from flask import jsonify, abort, request

from api.v1.views import app_views


@app_views.route('/states', methods=['GET'])
def get_states():
    """ Gets all states """
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>',
                 methods=['GET'])
def get_state(state_id):
    """ Gets a state by id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a state by id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states',
                 methods=['POST'])
def create_state():
    """ Creates a state """
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['PUT'])
def update_state(state_id):
    """ Updates a state by id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')

    forbidden_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in forbidden_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
