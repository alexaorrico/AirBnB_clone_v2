#!/usr/bin/python3
"""
New view for State objects that handles all default RESTFul API actions
"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage, State

# Route to retrieve a list of all State objects
@app_views.route('/states', methods=['GET'])
def get_states():
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)

# Route to retrieve a specific State object by state_id
@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

# Route to delete a specific State object by state_id
@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

# Route to create a new State object
@app_views.route('/states', methods=['POST'])
def create_state():
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    
    new_state = State(**data)
    new_state.save()
    
    return jsonify(new_state.to_dict()), 201

# Route to update a specific State object by state_id
@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    
    # Ignore keys: id, created_at, updated_at
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    
    state.save()
    
    return jsonify(state.to_dict()), 200
