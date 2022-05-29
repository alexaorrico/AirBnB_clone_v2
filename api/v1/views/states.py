#!/usr/bin/python3
""" Create a new view for State objects that handles all
    default RESTFul API actions
"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def state_No(state_id=None):
    """ Retrieves the list of all State objects """
    lista = []
    if state_id is None:
        for value in storage.all("State").values():
            lista.append(value.to_dict())
        return jsonify(lista), 200
    else:
        state = storage.get("State", state_id)
        if state is None:
            abort(404)
        return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def state_del(state_id=None):
    """ delete a object if it is into states"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def post_states():
    """post method states, You must use request.get_json from Flask"""
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if "name" not in json_data.keys():
        return jsonify({'error': "Missing name"}), 400
    state = State(**json_data)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_states(state_id=None):
    """ method put Updates a State object: PUT """
    p_state = storage.get("State", state_id)
    if p_state is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in json_data.items():
        if key != "__class__":
            setattr(p_state, key, value)
    storage.save()
    return jsonify(p_state.to_dict()), 200
