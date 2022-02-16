#!/usr/bin/python3
""" State objects """

from flask import Flask, jsonify, abort, request, Response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states',  strict_slashes=False, methods=['GET'])
def get_states():
    """Retrieves the list of all State objects: GET /api/v1/states"""
    dict_state = storage.all(State)
    states_list = []
    for value in dict_state.values():
        states_list.append(value.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """Retrieves a State object """
    dict_state = storage.all(State)
    for key, value in dict_state.items():
        if "State.{}".format(state_id) == key:
            return jsonify(value.to_dict())
    abort(404)


@app_views.route(
    '/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    dict_state = storage.all(State)
    for key, value in dict_state.items():
        if "State.{}".format(state_id) == key:
            storage.delete(value)
            storage.save()
            return {}
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state():
    """Creates a State """
    if not request.get_json():
        abort(Response("Not a JSON", 400))
    elif "name" not in request.get_json():
        abort(Response("Missing name", 400))
    else:
        new_state = State(**request.get_json())
        storage.new(new_state)
        storage.save()
    return new_state.to_dict(), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def put_state(state_id):
    """Updates a State object"""
    if not request.get_json():
        abort(Response("Not a JSON", 400))
    else:
        try:
            request.get_json().pop("id")
        except:
            pass
        try:
            request.get_json().pop("created_at")
        except:
            pass
        try:
            request.get_json().pop("updated_at")
        except:
            pass

        state = storage.get('State', state_id)
        if state is None:
            abort(404)

        for key, value in request.get_json().items():
            setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
