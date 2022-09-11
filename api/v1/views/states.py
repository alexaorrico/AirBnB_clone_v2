#!/usr/bin/python3
"""variable app_views which is an instance of Blueprint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def states_get():
    """function for method get"""
    states = storage.all("State")
    states_list = []
    for value in states.values():
        states_list.append(value.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def states_id(state_id=None):
    """return state by id"""
    state = storage.get(State, state_id)
    if state is not None:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def states_delete(state_id=None):
    """delete state by id"""
    if state_id is not None:
        state = storage.get(State, state_id)
        if state is not None:
            storage.delete(state)
            storage.save()
            return {}, 200
        else:
            abort(404)


@app_views.route('/states/', methods=['POST'])
def states_post():
    """add new state"""
    response = request.get_json()
    if response is not None:
        if 'name' in response:
            new_state = State(**response)
            new_state.save()
            return jsonify(new_state.to_dict()), 201
        else:
            abort(400, description="Missing name")
    else:
        abort(400, description="Not a JSON")


@app_views.route('/states/<state_id>', methods=['PUT'])
def states_put(state_id=None):
    update object if exists
    state = storage.get(State, state_id)
    if state is not None:
        response = request.get_json()
        if response is not None:
            response.pop("id", None)
            response.pop("created_at", None)
            response.pop("updated_at", None)
            for key, value in response.items():
                setattr(state, key, value)
                storage.save()
                return jsonify(state.to_dict()), 200
        else:
            abort(404)
    else:
        abort(400, description="Not a JSON")
