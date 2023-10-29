from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    retrieves all State objects
    """
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    retrieves a State object
    Args:
        state_id: id of specific state
    """
    state = storage.get(State, state_id)
    if state:
        response = state.to_dict()
        return jsonify(response)
    abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    deletes a State object
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    abort(404)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    creates a State object from json data passed
    """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')

    data = request.get_json()
    state = State(**data)
    state.save()
    response = state.to_dict()
    return jsonify(response), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    updates a State object
    """
    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    state = storage.get(State, state_id)
    if state:
        ignore_attribute = ['id', 'created_at', 'updated_at']
        for attribute, value in data.items():
            if attribute not in ignore_attribute:
                setattr(state, attribute, value)
        state.save()
        response = state.to_dict()
        return jsonify(response), 200
    abort(404)
