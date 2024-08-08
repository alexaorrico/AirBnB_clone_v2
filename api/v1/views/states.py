#!/usr/bin/python3
"""
Module defines view for State objects that handles all default
RESTFul API actions.
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ Retrievs a list of all State objects """
    states_list = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State object of a specified state_id """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    else:
        return jsonify(state_obj.to_dict())


@app_views.route('states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ Deletes state object of a specified state_id """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    else:
        storage.delete(state_obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a state object """

    try:
        data = request.get_json()
    except BadRequest:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")
    else:
        state_obj = State(**data)
        storage.new(state_obj)
        storage.save()
        return jsonify(state_obj.to_dict()), 201


@app_views.route('states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates state """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    try:
        data = request.get_json()
    except BadRequest:
        abort(400, description="Not a JSON")

    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(state_obj, key, value)
    storage.save()
    return jsonify(state_obj.to_dict()), 200
