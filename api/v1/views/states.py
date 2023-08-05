#!/usr/bin/python3
"""file that return the status of the API"""
from api.v1.views import app_views
from flask import jsonify, make_response, request
from models import storage
from models.state import State
from flask import abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_of_states():
    """return the list of states"""
    states = storage.all("State")
    result = []
    for s in states.values():
        result.append(s.to_dict())
    return (jsonify(result))


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_state(state_id):
    """return a state specify
       state_id: id of the state to retreive
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return (jsonify(state.to_dict()))


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_state(state_id):
    """Delete a state specify
       state_id: id of the state to delete
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return (jsonify({}))


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """create a new state"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """update a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for at, val in request.get_json().items():
        if at not in ['id', 'created_at', 'updated_at']:
            setattr(state, at, val)
    state.save()
    return jsonify(state.to_dict())
