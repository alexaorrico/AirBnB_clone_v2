#!/usr/bin/python3
"""objects that handles all default RESTFul API actions"""

from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'])
def all_states():
    """Retrieves the list of all State objects"""
    all_states = storage.all(State).values()
    list_states = []
    for obj in all_states:
        list_states.append(obj.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<string:id>', methods=['GET'])
def get_states(id):
    """Retrieves a state_id object"""
    state = storage.get(State, id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:id>', methods=['DELETE'])
def del_state(id):
    """Deletes a State object"""
    state = storage.get(State, id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()
    return {}, 200


@app_views.route('/states', methods=['POST'])
def post_state():
    """Creates a State"""
    info = request.get_json()
    if not info:
        abort(400, description="Not a JSON")
    if 'name' not in info:
        abort(400, description="Missing name")
    new_state = State(**info)
    new_state.save()
    return new_state.to_dict(), 201


@app_views.route('/states/<string:id>', methods=['PUT'])
def put_state(id):
    """Updates a State object"""
    state = storage.get(State, id)
    if not state:
        abort(404)
    info_update = request.get_json()
    if not info_update:
        abort(400, description="Not a JSON")

    ignore_key = ["id", "created_at", "updated_at"]
    for key, value in info_update.items():
        if key not in ignore_key:
            setattr(state, key, value)
    state.save()

    return jsonify(state.to_dict()), 200
