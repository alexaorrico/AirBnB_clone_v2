#!/usr/bin/python3
""" flask module to manage the stored states """
from models.state import State
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage


@app_views.route(
    '/states',
    strict_slashes=False,
    methods=['GET', 'POST']
)
@app_views.route(
    '/states/<state_id>',
    strict_slashes=False, methods=['GET', 'PUT', 'DELETE']
)
def states(state_id=None):
    """ handles all default RestFul API actions inside states"""
    if request.method == 'GET' and state_id is None:
        return all_states()
    elif request.method == 'GET' and state_id:
        return get_state(state_id)
    elif request.method == 'DELETE':
        return delete_state(state_id)
    elif request.method == 'POST':
        return create_state()
    elif request.method == 'PUT':
        return update_state(state_id)


def update_state(state_id):
    """ it update an state """
    ignored_keys = ['id', 'created_at', 'updated_at']
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_json = request.get_json()
    if state_json is None:
        abort(400, 'Not a JSON')

    for key in state_json.keys():
        if key in ignored_keys:
            continue
        if getattr(state, key):
            setattr(state, key, state_json[key])
        storage.save()
        return jsonify(state.to_dict()), 200


def create_state():
    """ it create an state from a http request
    the new state information is expected to be
    json string
    """
    state_json = request.get_json()
    if state_json is None:
        abort(400, 'Not a JSON')
    if state_json.get('name') is None:
        abort(400, "Missing name")
    state = State(**state_json)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


def delete_state(state_id):
    """ it delete the state corresponding to the state_id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


def get_state(state_id):
    """ it get the state corresponding to the state_id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


def all_states():
    """ it retrieve all the states """
    states = storage.all(State)
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)
