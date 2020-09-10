#!/usr/bin/python3
"""
Task 7
Create a new view for State objects
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('/api/v1/states', strict_slashes=False)
def all_states():
    """Retrieves a list of all State objects"""
    all_states = []
    for state in storage.all('State').values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/api/v1/states/<state_id>', strict_slashes=False)
def retrieve_state(state_id):
    """Retrieves a State object"""
    try:
        state = jsonify(storage.get('State', state_id).to_dict())
        return state
    except:
        abort(404)


@app_views.route('/api/v1/states/<state_id>', strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get('State', state_id)
    if state:
        state.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/api/v1/states', strict_slashes=False)
def create_state():
    """Creates a State object"""
    state_list = request.get_json()
    if not state_list:
        abort(400, {'Not a JSON'})
    elif 'name' not in state_list:
        abort(400, {'Missing name'})
    new_state = State(**state_list)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/api/v1/states/<state_id>', strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    update_obj = request.get_json()
    if not update_obj:
        abort(400, {'Not a JSON'})
    this_state = storage.get('State', state_id)
    if not thi_state:
        abort(404)
    for key, value in update_obj.items():
        setattr(this_state, key, value)
    storage.save()
    return jsonify(this_state.to_dict())
