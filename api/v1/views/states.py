#!/usr/bin/python3
"""handles default RESTful API actions for State objects"""
from api.v1.views import app_views
from flask import jsonify, request, abort, Flask, make_response
from models import storage
from models.State import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_states(state_id=None):
    """Retrieves a state, all states, or posts one"""
    states = storage.all(State)

    if request.method == 'GET':
        if state_id is None:
            return jsonify([state.to_dict() for state in states.values()])

        state_grab = storage.get(State, state_id)
        if state_grab is None:
            abort(404)
        return jsonify(state_grab.to_dict())

    elif request.method == 'POST':
        state_data = request.get_json()
        if not state_data:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in state_data:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        state_add = State(**state_data)
        storage.save()
        return make_response(jsonify(state_add.to_dict()), 201)

    elif request.method == 'DELETE':
        stateToDelete = storage.get(State, state_id)
        if stateToDelete is None:
            abort(404)
        storage.delete(stateToDelete)
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'PUT':
        state_update = storage.get(State, state_id)
        if state_update is None:
            abort(404)
        if request.is_json:
            state_data = request.get_json()
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)

        for key, val in state_data.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(state_update, key, val)
        storage.save()
        return make_response(jsonify(state_update.to_dict()), 200)
