#!/usr/bin/python3
"""A new view for State objects"""
from api.v1.views import app_views
from models import state, storage
from flask import Flask, jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """Retrieves the list of all State objects"""
    all_states = storage.all('State').values()
    list_states = []

    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """Retrieves a State"""
    state = storage.get('State', state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                  strict_slashes=False)
def state_delete(state_id):
    """Deletes a State"""
    state = storage.get('State', state_id)
    if state:
        state.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def state_post():
    """Creates a State"""
    if not request.get_json():
        return jsonify({'message': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'message': 'Missing name'}), 400

    state = state.State(name=request.get_json().get('name'))
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_put(state_id):
    """Updates a State"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict())