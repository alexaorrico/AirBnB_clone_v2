#!/usr/bin/python3
"""
view for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states')
def get_states():
    """Retrieves the list of all State objects """
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>')
def get_state(state_id):
    """Retrieves a State object based onstate_id, raises a 404 error
    if state_id is not linked to any State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State Object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def add_state():
    """creates a State"""
    if not request.get_json(force=True, silent=True):
        return ("Not a JSON\n", 400)
    if 'name' not in request.get_json():
        return ("Missing name\n", 400)
    request_data = request.get_json()
    new_state = State(**request_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """updates a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json(force=True, silent=True):
        return ("Not a JSON\n", 400)
    request_data = request.get_json()
    request_data.pop('id', None)
    request_data.pop('created_at', None)
    request_data.pop('updated_at', None)
    for key, value in request_data.items():
        setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
