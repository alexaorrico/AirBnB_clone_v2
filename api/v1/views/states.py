#!/usr/bin/python3
"""Create a new view for State objects that handles all
default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_all_states():
    """Retrieves a list of all States"""
    data = storage.all('State')
    states = [v.to_dict() for k, v in data.items()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_specific_state(state_id):
    """Retrieves a specific instance of State, otherwise 404 error"""
    data = storage.all('State')
    name = 'State.' + state_id
    state = [v.to_dict() for k, v in data.items() if k == name]
    if len(state) != 1:
        abort(404)
    return jsonify(state[0])


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_specific_state(state_id):
    """Deletes a specific instance of State, otherwise 404 error"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Adds another object to the storage"""
    new_state_dict = request.get_json(silent=True)
    if new_state_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**new_state_dict)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates an instance of State"""
    update_state_json = request.get_json(silent=True)
    if update_state_json is None:
        return jsonify({'error': 'Not a JSON'}), 400
    states = storage.all('State')
    state = None
    for s in states:
        if state_id in s:
            state = states[s]
    if not state:
        abort(404)
    ignore = ['id', 'created_at', 'updated_at']
    for k, v in update_state_json.items():
        if k not in ignore:
            setattr(state, k, v)
            storage.save()
    return jsonify(state.to_dict())
