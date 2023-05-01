#!/usr/bin/python3
""" This module handles all default RESTFUL api actions for state objects"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False)
def all_state():
    """ Retrieves list of all State objects """
    state_lists = []
    for state_object in storage.all(State).values():
        objects = state_object.to_dict()
        state_lists.append(objects)
    return jsonify(state_lists)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_single_state(state_id):
    """ Retrieves a single state based on state id"""
    for state_object in storage.all(State).values():
        objects = state_object.to_dict()
        if state_id == objects['id']:
            return objects
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_object(state_id):
    """ Deletes a state object """
    state = storage.get(State, state_id)
    if state is not None:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_object():
    """ Creates a State """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    state = State(name=data['name'])
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_object(state_id):
    """ Updates a State object """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data.pop('id', None)
    data.pop('created_at', None)
    data.pop('updated_at', None)
    for key, value in data.items():
        setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
