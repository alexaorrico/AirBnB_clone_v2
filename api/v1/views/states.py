#!/usr/bin/python3
"""View for State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """return all the states in the database"""
    states_list = []

    for state in storage.all(State).values():
        states_list.append(state.to_dict())

    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """return a state by id in the database"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """delete a state by id in the database"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    state.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """create a new state in the database"""
    try:
        state_dict = request.get_json()
        if 'name' not in state_dict:
            return 'Missing name', 400

        new_state = State(**state_dict)
        new_state.save()
        return jsonify(new_state.to_dict()), 201
    except Exception:
        return 'Not a JSON', 400
