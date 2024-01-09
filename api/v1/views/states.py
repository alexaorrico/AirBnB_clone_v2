#!/usr/bin/python3
''' REST API blueprint for State class '''

from flask import Flask, jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    ''' returns all state objects in storage in json format '''
    states = [state.to_dict() for state in storage.all('State').values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    ''' find and returns state with macthing id '''
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_state(state_id):
    ''' deletes a state object with maching given state_id '''
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_new_state():
    ''' creates a new state object '''
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        obj = State(**data)
        obj.save()
        return (jsonify(obj.to_dict()), 201)


@app_views.route('/states/<states_id>', methods=['PUT'], strict_slashes=False)
def update_state(states_id):
    ''' updates an existing state object '''
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
    return (jsonify(obj.to_dict()), 200)
