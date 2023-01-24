#!/usr/bin/python3
""" This module contains the states view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def handle_states():
    """ Retrieves the list of all State objects """
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201
    elif request.method == 'GET':
        states = storage.all('State')
        states_list = []
        for state in states.values():
            states_list.append(state.to_dict())
        return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def handle_state(state_id):
    """ Retrieves a State object """
    state = storage.get('State', state_id)
    if state is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    elif request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({}), 200
