#!/usr/bin/python3
"""
a new view for State objects
that handles all default RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ retrieves the list of all State objects """
    states = storage.all(State).values()
    json_states = [state.to_dict() for state in states]
    return jsonify(json_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ retrieves a State object (specified with state_id) """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ deletes a State object (specified with state_id) """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ creates a State object """
    state_data = request.get_json()
    if not state_data:
        abort(400, "Not a JSON")
    if 'name' not in state_data:
        abort(400, "Missing name")
    new_state = State(**state_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ updates a State object (specified with state_id) """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_data = request.get_json()
    if not state_data:
        abort(400, "Not a JSON")
    for key, value in state_data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
