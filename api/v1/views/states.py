#!/usr/bin/python3
"""State view model"""
from flask import abort
from flask import jsonify
from flask import request
from flask import make_response
from models.state import State
from api.v1.views import app_views


states = State().to_dict()


@app_views.errorhandler(404)
def not_found(error):
    """ 404 - Not found function """
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/states', methods=['GET'])
def get_states():
    """Returns all state objects."""
    return jsonify(states,)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Returns a specified state object."""
    state_id = "State." + state_id

    if state_id not in states.keys():
        abort(404)

    return jsonify(states[state_id],)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a specified state object."""
    state_id = "State." + state_id

    if state_id not in states.keys():
        abort(404)

    del states[state_id]
    return jsonify({}), 200, {'ContentType': 'application/json'}


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a new state object."""
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.get_json().keys():
        abort(400, 'Missing name')

    return State(**request.get_json()), 201


@app_views.route('/states/<state_id>', methods=["PUT"])
def update_state(state_id):
    """Modifies a state object."""
    state_id = "State." + state_id

    if not request.json:
        abort(400, "Not a JSON")
    if state_id not in states.keys():
        abort(404)

    states[state_id]['name'] = \
        request.get_json.get('name', states[state_id]['name'])
    states[state_id]['__class__'] = request.get_json.get(
        'name', states[state_id]['__class__'])

    return states[state_id], 200, {'ContentType': 'application/json'}
