#!/usr/bin/python3
""" retruns json response status of API """
from flask import Flask, abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    ''' gets list of all state objects '''
    states_list = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    return jsonify(state_object.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delte_state(state_id):
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    storage.delete(state_object)
    storage.save()
    return make_response(jsonify({}))

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    response = request.get_json()
    if not response:
        return jsonify({'Not a JSON'}), 400
    if "name" not in response:
        return jsonify({'Missing name'}), 400
    new_state = State(**response)
    new_state.save()
    return jsonify(new_state.to_dict()), 201
   

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(400)
    response = request.get_json()
    if not response:
        return jsonify({'Not a JSON'}), 400
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in response.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
        
    
    

