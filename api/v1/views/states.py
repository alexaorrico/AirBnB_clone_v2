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
@app_views.route('/states/<state_id>', methods=['GET'])
def retrieve_state(state_id=None):
    """ Retrieves the list of all State objects:"""
    all_states_obj = storage.all(State).values()
    if state_id is None:
        states_list = []
        for item in all_states_obj:
            states_list.append(item.to_dict())
        return jsonify(states_list)
    else:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
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
        abort(400, '{"error": "Not a JSON"}')
    elif 'name' not in request_data:
        abort(400, '{"error": "Missing name"}')

    new_state = State()
    new_state.name = request_data['name']
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ Updates a State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, '{"error": "Not a JSON"}')

    state_dict = state.to_dict()
    for key, value in request_data.items():
        state_dict[key] = value
    storage.save()
    return make_response(storage.get(State, state_id), 200)
