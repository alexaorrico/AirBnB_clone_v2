#!/usr/bin/python3
""" objects that handles all default RestFul API actions for States """
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """
    Retrieves the list of all State objects
    or a specific State
    """

    if not state_id:
        all_states = storage.all(State).values()
        list_states = []
        for state in all_states:
            list_states.append(state.to_dict())
        return jsonify(list_states)
    else:
        state = storage.get(State, state_id)
        if not state:
            abort(404)

        return jsonify(state.to_dict())


@app_views.route('states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State Object
    """

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """
    Creates a State
    """
    if not request.json:
        abort(400, description="Not a JSON")

    if 'name' not in request.json:
        abort(400, description="Missing name")

    data = request.json
    instance = State(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    Updates a State
    """
    if not request.json:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    data = request.json
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
