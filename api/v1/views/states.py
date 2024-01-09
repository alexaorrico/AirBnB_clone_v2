#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """gets all states"""
    return jsonify([x.to_dict() for x in storage.all('State').values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """gets state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """deletes state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return {}, 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    body = request.get_json()

    if not body:
        return jsonify({'message': 'Not a JSON'}), 400

    if 'name' not in body:
        return jsonify({'message': 'Missing name'}), 400

    new_state = State(name=body.get('name'))
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updates state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        return abort(400, 'Not a JSON')
    for k, v in data.items():
        if key not in [id, 'created_at', 'updated_at']:
            setattr(state, k, v)
    storage.save()
    return jsonify({state.to_dict()}), 200
