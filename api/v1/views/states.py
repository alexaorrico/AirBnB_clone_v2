#!/usr/bin/python3
"""states view"""
from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def states():
    """display all states"""
    return jsonify([obj.to_dict() for obj in storage.all(State).values()])


@app_views.route('/states/<id>', methods=['GET'])
def state_by_id(id):
    """display state by id"""
    state = storage.get(State, id)
    if state:
        return state.to_dict()
    return abort(404)


@app_views.route('/states/<id>', methods=['DELETE'])
def delete_state(id):
    """delete a state by its id"""
    state = storage.get(State, id)
    if state:
        storage.delete(state)
        storage.save()
        return {}
    return abort(404)


@app_views.route('/states', methods=['POST'])
def create_state():
    """create a new state"""
    if request.is_json:
        data = request.get_json()
        if not data.get('name'):
            abort(400, 'Missing name')
        new_state = State(**data)
        new_state.save()
        return new_state.to_dict(), 201

    abort(400, 'Not a JSON')


@app_views.route('/states/<id>', methods=['PUT'])
def update_state(id):
    """update a state by its id"""
    state = storage.get(State, id)
    if not state:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    storage.save()
    return state.to_dict()
