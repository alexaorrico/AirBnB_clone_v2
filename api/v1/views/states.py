#!/usr/bin/python3
"""State management endpoints"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from datetime import datetime
import uuid


@app_views.route('/states/', methods=['GET'])
def list_states():
    '''Fetches all State objects'''
    state_list = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    '''Fetches a specific State object by ID'''
    all_states = storage.all("State").values()
    matching_state = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if not matching_state:
        abort(404)
    return jsonify(matching_state[0])


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    '''Deletes a specific State object by ID'''
    all_states = storage.all("State").values()
    matching_state = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if not matching_state:
        abort(404)
    matching_state.remove(matching_state[0])
    for obj in all_states:
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def create_state():
    '''Creates a new State object'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    state_list = []
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    state_list.append(new_state.to_dict())
    return jsonify(state_list[0]), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    '''Updates an existing State object'''
    all_states = storage.all("State").values()
    matching_state = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if not matching_state:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    matching_state[0]['name'] = request.json['name']
    for obj in all_states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(matching_state[0]), 200
