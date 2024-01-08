#!/usr/bin/python3
'''
    RESTful API for class State
'''

from flask import Flask, jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_state():
    '''
        return state in json form
    '''
    state_list = [s.to_dict() for s in storage.all('State').values()]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    '''
        return state and its id using http verb GET
    '''
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_state(state_id):
    '''
        delete state obj given state_id
    '''
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''
        create new state obj
    '''
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        obj = State(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/states/<states_id>', methods=['PUT'], strict_slashes=False)
def update_state(states_id):
    '''
        update existing state object
    '''
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    obj = storage.get("State", states_id)
    if obj is None:
        abort(404)
    for attr, value in data:
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(obj, attr, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
