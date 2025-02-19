#!/usr/bin/python3
""" Create a new view for State objects that handles all default RESTFul API
"""
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects: GET /api/v1/states
    """
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object: GET /api/v1/states/<state_id>
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route(
        '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object:: DELETE /api/v1/states/<state_id>
    """

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    state.delete()
    storage.save()

    return (jsonify({}))


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """
    Creates a State: POST /api/v1/states
    """
    obj = request.get_json(silent=True)

    if not obj:
        abort(400, description="Not a JSON")

    if 'name' not in obj:
        abort(400, description="Missing name")

    instance = State(**obj)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    Updates a State object: PUT /api/v1/states/<state_id>
    """
    state = storage.get(State, state_id)
    obj = request.get_json(silent=True)

    if not state:
        abort(404)

    if not obj:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in obj.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
