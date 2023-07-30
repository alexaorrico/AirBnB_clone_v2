#!/usr/bin/python3
"""
Module to handle all default RESTFul API actions for State objects.
"""
from flask import jsonify
from flask import abort
from flask import request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def get_states():
    """
    Retrieves the list of all State objects and returns them in JSON format.
    """
    states_list = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(states_list)


@app_views.route('/states/<int:state_id>', methods=['GET'])
def get_state(state_id):
    """
    Retrieves and returns State object with the given state_id.
    If not found, raise 404 error.
    """
    state = [obj.to_dict() for obj in storage.all(State).values()
             if obj.id == state_id]
    if not state:
        abort(404)
    return jsonify(state[0])


@app_views.route('/states/<int:state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes State object with the given state_id.
    If not found, raise 404 error.
    """
    states = storage.all(State).values()
    state = [obj.to_dict() for obj in states if obj.id == state_id]
    if not state:
        abort(404)
    state.remove(state[0])
    for obj in states:
        if obj.id == state_id:
            storage.delete(state)
            storage.save()
    return jsonify({}), 200


@app_views.route('/states')
def create_state():
    """
    Creates a State and returns the new State with status code 201.
    """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    new_state = State(name=request.get_json['name'])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<int:state_id>', methods=['PUT'])
def update_state(state_id):
    """
    Updates the state with the given state_id.
    Ignores id, created_at, updated_at keys.
    """
    states = storage.all(State).values()
    state = [obj.to_dict() for obj in states if obj.id == state_id]
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state[0]['name'] = request.json['name']

    for obj in states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state[0]), 200
