#!/usr/bin/python3
"""
handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """
    Retrieves the list of all State objects
    """
    all_states = []
    for state in storage.all("State").values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_state(state_id):
    """
    Retrieves a State object
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a state
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict())
