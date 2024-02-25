#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects"""
    all_states = []
    states = storage.all(State).values()
    for state in states:
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_by_id(state_id):
    """Retrieves the list of State object by its id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_by_id(state_id):
    """function that delete State object by its id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """function that create state object"""
    if not request.is_json:
        return make_response("Not a JSON", 400)
    request_data = request.get_json()
    if 'name' not in request_data:
        abort(400, 'Missing name')
    new_state = State(**request_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """function that updates a State object"""
    if not request.is_json:
        return make_response("Not a JSON", 400)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    request_data = request.get_json()
    ignored_keys = ["id", "created_at", "updated_at"]
    for key, value in request_data.items():
        if key not in ignored_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
