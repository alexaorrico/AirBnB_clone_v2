#!/usr/bin/python3
""" Objects that handels all default RestFul API actions for state """
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET'], sstrict_slashes=False)
def get_states():
    """ Retrieves the list of all state objects """
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieve a specific State """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/state/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object """

    state = storage.get(State, state_id)

    if not state:
        abort (404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a State """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instanse = State(**data)
    instanse.save()
    return make_response(jsonify(instanse.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Update a State """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)