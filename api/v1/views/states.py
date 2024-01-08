#!/usr/bin/python3
""" The module handles the default RESTful API acstions """

# Import the required Modules
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


# Route for retrieving all state objs
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """
    GETs all state objects
    """
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)


# Route for retrieving specific stated by their id
@app_views.route(
    '/states/<string:state_id>',
    methods=['GET'],
    strict_slashes=False
)
def get_state(state_id):
    """
    GETs a specified state
    """
    state = storage.get("State", state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


# Route for deleting a specific State by id
@app_views.route(
    '/states/<string:state_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_state(state_id):
    """
    DELETEs a state by their id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return (jsonify({}), 200)


# Route for creating a new state
@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """ POSTs in a new state """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


# Route for updating an existing state
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates an existing state
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(state, attr, val)
    state.save()
    return jsonify(state.to_dict())
