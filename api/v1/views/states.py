#!/usr/bin/python3
""" Scripts starts a flask application"""

from flask import Flask, jsonify
from api.v1.views  import app_views
from models import storage
from models.state import State

@app_views.route('/api/v1/states', methods=['GET'], strict_slashes=False)

def show_all_states():
    """gets all state objects and displays them"""
    state_list = []
    for i in storage.all('State').values():
        state_list.append(i.to_dict())

    return jsonify(state_list)

@app_views.route('/api/v1/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def show_single_state(state_id):
    """ get a specific state by its id """
    state = storage.get('State', state_id)
    if state is not None:
        return jsonify(state.to_dict())
    else:
        abort(404)

@app_views.route('/api/v1/states', methods=['POST'],
                 strict_slashes=False)

def state_create():
    """create a new state"""
    state = request.get_json()
    if state is None:
        abort(404, 'Not a JSON')
    if 'name'not in state:
        abort(404, 'missing name')
    created_state = State(state)
    created_state.save()
    return jsonify(created_state)

@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)

def delete_state(state_id):
    """delete an existing state by its id"""
    delete_state = storage.get('State', state_id)
    if delete_state is not None:
        delete_state.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/api/v1/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)

def updated_state(state_id):
    """ updates information about a state"""
    state = request.get_json()
    if state is None:
        abort(404, 'Not a JSON')
    updated_state = storage.get('State', state_id)
    if updated_state is None:
        abort(404)

        
