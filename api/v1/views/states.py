#!/usr/bin/python3
"""states"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def list_states():
    '''GET all State'''
    states = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    '''GET State '''
    all_states = storage.all("State").values()
    states = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if states == []:
        abort(404)
    return jsonify(states[0])


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    '''DELETE State'''
    all_states = storage.all("State").values()
    states = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if states == []:
        abort(404)
    states.remove(states[0])
    for obj in all_states:
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def create_state():
    '''POST a State'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states = []
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    states.append(new_state.to_dict())
    return jsonify(states[0]), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def updates_state(state_id):
    '''Updates a State object'''
    all_states = storage.all("State").values()
    states = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if states == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    states[0]['name'] = request.json['name']
    for obj in all_states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(states[0]), 200
