#!/usr/bin/python3
'''state view'''
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    '''Return all the states in the storage'''
    state_object = storage.all(State)
    return jsonify([object.to_dict() for object in state_object.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def search_by_id(state_id):
    '''Filter state by id'''
    object = storage.get(State, state_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_obj(state_id):
    '''Delete state of the provided id'''
    object = storage.get(State, state_id)
    if object is None:
        abort(404)
    else:
        storage.delete(object)
        storage.save()
        # Return an empty dictionary with status code 200
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''Create a new state'''
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()
        # method extracts and parses data from request body
        # if data is in json format, it return python dict or list
        # If the data is not valid JSON, raise an error or return None
        if 'name' not in data:
            abort(400, 'Missing name')
        new_state = State(**data)
        # Create a new instance of state and pass the key value pairs
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201
    else:
        abort(400, 'Not a JSON')


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''Update state of provided id'''
    object = storage.get(State, state_id)
    if object is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    else:
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(object, key, value)
        storage.save()
        return jsonify(object.to_dict()), 200