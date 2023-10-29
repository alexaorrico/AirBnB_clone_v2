#!/usr/bin/python3

"""view for State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new state object"""
    if not request.get_json():
        abort(400, {'message': 'Not a JSON'})
    if 'name' not in request.get_json():
        abort(400, {'message': 'Missing name'})
    state = State(**request.get_json())
    state.save()
    return (jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, {'message': 'Not a JSON'})
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return (jsonify(state.to_dict()), 200)
