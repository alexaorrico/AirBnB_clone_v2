#!/usr/bin/python3
"""this module handles all default RESTFul API actions"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views

import models
from models.state import State

@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    all_states = models.storage.all(State)
    man = [x.to_dict() for x in all_states.values()]
    return jsonify(man)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    state = models.storage.get(State, state_id)
    if state is not None:
        return jsonify(state.to_dict())
    abort(404)
    

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    state = models.storage.get(State, state_id)
    if state is not None:
        models.storage.delete(state)
        models.storage.save()
        return {}, 200
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    try:
        data = request.get_json()
        print(data)
        if "name" not in data.keys():
            abort(404, descripton='Missing name')
        new_state = State(**data)
        models.storage.new(new_state)
        models.storage.save()
        return jsonify(new_state.to_dict()), 201
    except Exception as ep:
        abort(400, description='Not a JSON')
