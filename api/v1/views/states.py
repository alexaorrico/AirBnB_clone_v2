#!/usr/bin/python3
""" State view"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get method for states view"""
    _states = storage.all(State)
    return jsonify([obj.todict() for obj in _states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """get method for a particular state"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """delete method for a particular state"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    state.delete()
    state.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """post method for state object"""
    new_state = request.get_json()
    if not request.json:
        abort(400, "Not a JSON")
    if not 'name' in request.json:
        abort(400, "Missing name")
    state = State(**new_state)
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

    for k, v in body_request.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(state, k, v)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
