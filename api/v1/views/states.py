#!/usr/bin/python3
"""import modules
"""
from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'])
def get_states():
    """Retrives the list of all State objects
    """
    objs = storage.all(State).values()
    states_list = [state.to_dict() for state in objs]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_by_id(state_id):
    """Retrives State object by id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def post_state():
    """Creates a State
    """
    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    if 'name' not in data:
        abort(400, "Missing name")

    new_state = State(**data)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update a State object
    """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(state, key, value)

    storage.save()

    return jsonify(state.to_dict()), 200
