#!/usr/bin/python
""" Module efor state object view """

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
    return jsonify({})


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def post_state():
    """ Method creates new state object """
    return jsonify({"hi":"hi"})
    try:
        body = request.get_json()
    except Exception as e:
        abort(400, "Not a JSON")
    if body.get("name") == None:
        abort(400, "Missing name")
    state = State(body)
    storage.new(state)
    return state, 201
