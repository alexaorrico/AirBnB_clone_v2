#!/usr/bin/python3
"""
API version 1 views
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State


def handle_E(error=None, message="Not found", code=404):
    """Custom handler for 404 errors."""
    response = jsonify({"error": message})
    response.status_code = code
    return response


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def handle_API(state_id=None):
    """
    returns a state if state_id provided, otherwise all states"""
    if request.method == 'GET':
        return get_states(state_id)
    if request.method == 'DELETE':
        return delete_state(state_id)
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            return handle_E(message="Not a JSON", code=400)
        if data.get('name') is None:
            return handle_E(message="Missing name", code=400)
        return add_state(data)
    if request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            return handle_E(message="Not a JSON", code=400)
        if data.get('name') is None:
            return handle_E(message="Missing name", code=400)
        return update_state(state_id, data)


def get_states(state_id=None):
    """
    returns a state if state_id provided, otherwise all states"""
    try:
        if state_id:
            tmp = storage.get(State, state_id)
            if tmp is None:
                raise KeyError()
            tmp = State.to_dict(tmp)
        else:
            tmp = [State.to_dict(obj) for obj in storage.all(State).values()]
        print(tmp)
        return jsonify(tmp)
    except KeyError:
        return handle_E()


def delete_state(state_id=None):
    """delete state object"""
    st = storage.get(State, state_id)
    if st:
        tmp = State.delete(st)
        return jsonify({})
    else:
        return handle_E()


def add_state(data=None):
    """add new state object"""
    if data.get('name') is None:
        return handle_E(message="Missing name", code=400)
    st = State(data.get('name'))
    storage.new(st)
    tmp = State.to_dict(st)
    tmp['status_code'] = 201
    return jsonify(tmp)


def update_state(state_id, data):
    """add new state object"""
    st = storage.get(State, state_id)
    if st is None:
        return handle_E()

    data = request.get_json(silent=True)
    if data is None:
        return handle_E(message="Not a JSON", code=400)
    if data.get('name') is None:
        return handle_E(message="Missing name", code=400)
    st = State(data.get('name'))
    storage.new(st)
    tmp = State.to_dict(st)
    tmp['status_code'] = 201
    return jsonify(tmp)
