#!/usr/bin/python3
"""
This Module contains a view for state objects
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects """
    states_objs = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(states_objs)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """This retrieves the a state based of its ID """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state object based on a given ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """Creates a new state """
    request_json = request.get_json()
    required_key = "name"

    if not request_json:
        abort(400, "Not a JSON")
    if required_key not in request_json:
        abort(400, "Missing name")

    state = State(**request_json)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ this update a state object based on its state ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    request_json = request.get_json()
    if not request_json:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in request_json.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
