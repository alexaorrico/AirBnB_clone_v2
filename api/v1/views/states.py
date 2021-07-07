#!/usr/bin/python3
"""
 New view for State objects that handles all default RestFul API actions.
"""
from models.base_model import BaseModel
from models.state import State
from models import storage
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'])
def all_states():
    """ Retrieves the list of all State objects. """
    list_of_states = []
    for value in storage.all('State').values():
        list_of_states.append(value.to_dict())
    return jsonify(list_of_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def specific_state(state_id):
    """ Retrieves a State object. """
    if state_id:
        for value in storage.all('State').values():
            if state_id == value.id:
                return jsonify(value.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object. """
    if state_id:
        full_state = storage.get('State', state_id)
        storage.delete(full_state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'])
def create_state():
    """ Creates a State. """
    dic = request.get_json()
    if not dic:
        abort({'Not a JSON'}, 400)
    if 'name' not in dic:
        abort({'Missing name'}, 400)
    new_state = State(**dic)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('states/<state_id>', methods=['PUT'])
def updates_state(state_id):
    """ Updates a State object. """
    dic = request.get_json()
    selected_state = storage.get('State', state_id)
    if not selected_state:
        abort(404)
    if not dic:
        abort({'Not a JSON'}, 400)
    for key, value in dic.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(selected_state, key, value)
    storage.save()
    return jsonify(selected_state.to_dict()), 200
