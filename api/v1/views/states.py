#!/usr/bin/python3
""" Defines API endpoints for State objects """
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_state.yml', methods=['GET'])
def get_states():
    """ Returns a list of all State objects """
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_id_state.yml', methods=['get'])
def get_state(state_id):
    """ Returns a specific State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/state/delete_state.yml', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('documentation/state/post_state.yml', methods=['POST'])
def create_state():
    """ Creates a new State object """
    if not request.is_json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, description='Missing name')
    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/state/put_state.yml', methods=['PUT'])
def update_state(state_id):
    """ Updates a State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
