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
    ''' gets specific state objects by its state ID '''
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    return jsonify(state_object.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    ''' deletes state object '''
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    storage.delete(state_object)
    storage.save()
    return make_response(jsonify({}))


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''' creates a state '''
    response = request.get_json(silent=True)
    if not response:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in response:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_state = State(**response)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''' updates a state object '''
    state = storage.get(State, state_id)
    response = request.get_json(silent=True)
    if not state:
        abort(404)
    if not response:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in response.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return make_response(state.to_dict(), 200)
