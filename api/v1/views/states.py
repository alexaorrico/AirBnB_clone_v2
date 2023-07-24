#!/usr/bin/python3
"""
a new view for State objects
that handles all default RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """ retrieves the list of all State objects """
    states = storage.all("State")
    states_list = [state.to_dict() for state in states.values()]
    return jsonify(states_list)


@app_views.route('api/v1/views/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ retrieves a State object (specified with state_id) """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return state.to_dict()


@app_views.route('api/v1/views/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ deletes a State object (specified with state_id) """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """ creates a State object """
    state_data = request.get_json()
    if not state_data:
        abort(400, description="Not a JSON")
    if 'name' not in state_data:
        abort(400, description="Missing name")
    new_state = State(name=state_data['name'])
    return jsonify(new_state.to_dict()), 201


@app_views.route('api/v1/views/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ updates a State object (specified with state_id) """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state_data = request.get_json()
    if state_data is None:
        abort(400, description="Not a JSON")
    for key, value in state_data.items():
        if key in ('id', 'created_at', 'updated_at'):
            state.__setattr__(key, value)
    state.save()
    return jsonify(state.to_dict()), 200
