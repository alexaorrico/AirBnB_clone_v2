#!/usr/bin/python3
"""This module handles all default RestFul for state object"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieve_all_states():
    """
    """
    all_states = []
    for value in storage.all("State").values():
        all_states.append(value.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def retrieve_state_id(state_id):
    """
    """
    state = (storage.get('State', state_id))
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def Delete_state(state_id):
    """
    """
    state = storage.get('State', state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def Post_state():
    """
    """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    instance = State(**request.get_json())
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    """
    keys = ['id', 'created_at', 'updated_at']
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key in keys:
            pass
        else:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
