#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ Retrieves all State objects """
    list_states = storage.all(State)
    return jsonify([obj.to_dict() for obj in list_states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """ Retrieves a State id object """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a State object """
    new_data = request.get_json()
    if not new_data:
        abort(400, "Not a JSON")
    if "name" not in new_data:
        abort(400, "Missing name")
    state = State(**new_data)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Updates a State object """
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for key, value in body_request.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
