#!/usr/bin/python3
"""Module for State objects that handles
default RESTFul API"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """function that retrieves a list of all states"""
    states = storage.all(State).values()
    return jsonify([obj.to_dict() for obj in states])


@app_views.route('/states/<states_id>', methods=['GET'],
                 strict_slashes=False)
def get_states_id(states_id):
    """function that retrieves a State object"""
    state = storage.get(State, states_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """function that deletes a State when an id is a
    State id"""
    id = storage.get(State, state_id)
    if not id:
        abort(404)
    storage.delete(id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def post_state():
    """function that creates"""
    json_new_state = request.get_json(silent=True)
    if not json_new_state:
        abort(400, "Not a JSON")

    if 'name' not in json_new_state:
        abort(400, 'Missing name')

    new_state = State(json_new_state)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """function that update the State object
    in the dictionary"""
    id = storage.get(State, state_id)
    if not id:
        abort(404)

    new_state = request.get_json(silent=True)
    if not new_state:
        abort(400, "Not a JSON")

    state = storage.get(State, state_id)
    if 'name' in new_state:
        state.name = new_state['name']

    storage.save()
    return jsonify(state.to_dict()), 200
