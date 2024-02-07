#!/usr/bin/python3
"""contains State module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get.yml', methods=['GET'])
def all_state():
    """Retrieves state objects by id"""
    all_state = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(all_state)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/state/get_id.yml', methods=['GET'])
def get_state(state_id):
    """gets state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('documentation/state/post_id.yml', methods=['POST'])
def add_state():
    """adds a state object"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if not data['name']:
        abort(400, 'Missing name')
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/state/PUT.yml', methods=['PUT'])
def update_state(state_id):
    """adds a state object"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    for k, v in data.items():
        if k not in ('id', 'created_at', 'updated_at'):
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/state/delete.yml', methods=['DELETE'])
def del_method(state_id):
    """deletes state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200
