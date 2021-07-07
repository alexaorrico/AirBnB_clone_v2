#!/usr/bin/python3
""" This is a module that defines the states view
"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import request, jsonify, make_response, abort


@app_views.route('/states', methods=['GET', 'POST'])
def state_route():
    '''Returns a JSON of a state object'''
    if request.method == 'GET':
        '''GET retrieves from db a list of states'''
        states = storage.all('State').values()
        state_list = []
        for state in states:
            state_list.append(state.to_dict())
        return jsonify(state_list)
    if request.method == 'POST':
        '''POST adds a new state object to the db'''
        new_state = request.get_json()
        if new_state is None:
            abort(400, 'Not a JSON')
        if "name" not in new_state:
            abort(400, 'Missing name')
        new_state_obj = State(**new_state)
        new_state_obj.save()
        return jsonify(new_state_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def state_id_route(state_id):
    '''Retrieves a state object'''
    states = storage.get("State", state_id)
    if states is None:
        abort(404)
    if request.method == 'GET':
        '''GET retrieves from db a specific state object'''
        return jsonify(states.to_dict())
    if request.method == 'DELETE':
        '''DELETE removes from db the specific state object'''
        storage.delete(states)
        storage.save()
        return {}, 200
    if request.method == 'PUT':
        '''PUT updates the state object with name of the state changed'''
        state_put = request.get_json()
        if state_put is None:
            abort(400, 'Not a JSON')
        ignore_keys = ["id", "created_at", "updated_at"]
        for key, val in state_put.items():
            if key not in ignore_keys:
                setattr(states, key, val)
                states.save()
        return make_response(jsonify(states.to_dict()), 200)
