#!/usr/bin/python3
""" This module handles the HTTP methods of a state object"""
from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views

all_states = storage.all('State')
states = []

for state in all_states.values():
    states.append(state.to_dict())


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """ Handles HTTP request of all the state object """

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        state = State(name=data.get('name'))
        state.save()
        return jsonify(state.to_dict()), 201

    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_state(state_id=None):
    """ Handles HTTP requests of a single state object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        data['id'] = state.id
        data['created_at'] = state.created_at
        state.__init__(**data)
        state.save()
        return jsonify(state.to_dict()), 200

    return jsonify(state.to_dict())
