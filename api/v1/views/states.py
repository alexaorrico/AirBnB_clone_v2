#!/usr/bin/python3
'''
Import Blueprint to create routes for State
'''
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Get all register from table states
    ---
    response:
        200:
            description: List all states
    """
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def show_state(state_id):
    """Show a state filter by id
    ---
    parameters:
        - name: state_id
          in: path
          type: string
          required: true
    response:
        200:
            description: List a state filtered by state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a register from table states
    ---
    parameters:
        - name: state_id
          in: path
          type: string
          required: true
    response:
        200:
            description: Delete a state filtered by state_id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''Create new state for the table states'''
    state = request.get_json()
    if not state:
        abort(400, {'Not a JSON'})
    if 'name' not in state:
        abort(400, {'Missing name'})
    new_state = State(**state)
    storage.new(new_state)
    storage.save()
    return new_state.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''Update a register from table state filtered by id'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req = request.get_json(silent=True)
    if req is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for k, v in req.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(state, k, v)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
