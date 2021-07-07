#!/usr/bin/python3
""" Module for state object view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'],
                 strict_slashes=False)
def get_states():
    """ Returns all state object """
    states_dict_list = [state.to_dict() for
                        state in storage.all("State").values()]
    return jsonify(states_dict_list)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_id(state_id):
    """ Method retrieves state object with certain id """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Method deletes state object based off of its id """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def post_state():
    """ Method creates new state object """
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if body.get("name") is None:
        abort(400, "Missing name")
    state = State(**body)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """ Method updates a state object based off its id """
    state = storage.get("State", state_id)
    body = request.get_json()
    if not state:
        abort(404)
    if not body:
        abort(400, "Not a JSON")
    for k, v in body.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict())
