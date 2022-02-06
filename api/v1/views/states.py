#!/usr/bin/python3
""" Module which represents view for State objects that handles all default
RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.base_model import BaseModel
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retureve_states():
    """ Retrieves the list of all State objects"""
    all_states_obj = storage.all(State).values()
    states_list = []
    for item in all_states_obj:
        states_list.append(item.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def retrieve_state(state_id=None):
    """ Retrieves a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a State """
    request_data = request.get_json()

    if not request_data:
        abort(400, description="Not a JSON")
    elif 'name' not in request_data:
        abort(400, description="Missing name")

    new_state = State()
    new_state.name = request_data['name']
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in request_data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
