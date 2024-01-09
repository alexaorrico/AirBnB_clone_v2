#!/usr/bin/python3
"""
This is the states page endpoints
"""

from api.v1.views import app_views
from flask import jsonify, request
from werkzeug.exceptions import NotFound
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'])
def fetch_states(state_id=None):
    """Fetches all State objects from the database"""
    states = storage.all(State)
    if state_id:
        for state in states.values():
            state = state.to_dict()
            if state['id'] == state_id:
                return jsonify(state)
        raise NotFound
    return jsonify([object.to_dict() for object in states.values()])


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state obj using the state id"""
    states = storage.all(State)
    if state_id:
        for state in states.values():
            if state.id == state_id:
                storage.delete(state)
                storage.save()
                return jsonify({}), 200
    raise NotFound


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new state and saves it to the db"""
    state = request.get_json()
    if not state:
        return jsonify(error='Not a JSON'), 400
    if 'name' not in state:
        return jsonify(error='Missing name'), 400
    state = State(**state)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """This method updates a state's data"""
    state = storage.get(State, state_id)
    if not state:
        raise NotFound
    new_state = request.get_json()
    if not new_state:
        return jsonify(error='Not a JSON'), 400

    for key, value in new_state.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200
