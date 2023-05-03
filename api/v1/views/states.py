#!/usr/bin/python3
"""State file for views module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get():
    """Retrieve all state class"""
    states_list = []
    for item in storage.all("State").values():
        states_list.append(item.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_by_id(state_id):
    """Get a state object by id"""
    result = storage.get("State", state_id)
    if result is None:
        abort(404)
    return jsonify(result.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False
                 )
def delete(state_id):
    """Delete state by id"""
    result = storage.get("State", state_id)
    if result is None:
        abort(404)
    result.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create():
    """Create a new state object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    state_data = request.get_json()
    new_state = State(**state_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update(state_id):
    """Updates a state object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    old_data = storage.get("State", state_id)
    if old_data is None:
        # state to update does not exist
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(old_data, k, v)
    storage.save()
    return jsonify(old_data.to_dict())
