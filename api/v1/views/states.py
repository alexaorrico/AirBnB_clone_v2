#!/usr/bin/python3

""" Module for states
"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def all_states():
    """
    Return list of the all states
    """
    states_list = []
    states_obj = storage.all("State")
    for _, value in states_obj.items():
        states_list.append(value.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>')
def state(state_id):
    """
    Return  a state with the id
    """
    state = storage.get("State", state_id)
    if state is not None:
        return jsonify(state.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_state(state_id):
    """
    Delete a state with id
    """
    state = storage.get("State", state_id)
    if state is not None:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """
    Create a new object state
    """
    if not request.get_json():
        return make_response(jsonify({"error": 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": 'Missing name'}), 400)
    state = request.get_json()
    new_state = State(**state)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """
    Update a state by id
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": 'Not a JSON'}), 400)
    params = request.get_json()
    skip = ['id', 'created_at', 'updated_at']
    for key, value in params.items():
        if key not in skip:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())


@app_views.errorhandler(404)
def page_not_found(error):
    """
    Handle 404 error
    """
    return jsonify({"error": "Not found"}), 404
