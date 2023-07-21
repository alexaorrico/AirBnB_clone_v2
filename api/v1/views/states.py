#!/usr/bin/python3
"""
Module: index
"""
from api.v1.views import app_views, storage, State
from flask import jsonify, abort, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ returns all state objects in JSON format   """
    _states = [state.to_json() for state in storage.all('State').values()]
    return jsonify(_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_byID(state_id=None):
    """ returns a state object in JSON format  """
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return(jsonify(state.to_json()))


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_byID(state_id=None):
    """ delete state by id"""
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ creates a state  """
    json_obj = None
    try:
        json_obj = request.get_json()
    except:
        json_obj = None
    if json_obj is None:
        return "Not a JSON", 400

    if 'name' not in json_obj.keys():
        return "Missing name", 400
    state = State(**json_obj)
    state.save()
    return jsonify(state.to_json()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state_byID(state_id=None):
    """ update a state by id"""
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    try:
        request_data = request.get_json()
    except:
        request_data = None
    if request_data is None:
        return "Not a JSON", 400
    for item in ("id", "created_at", "updated_at"):
        request_data.pop(item, None)
    for k, v in request_data.items():
        setattr(state, k, v)
    state.save()
    return jsonify(state.to_json()), 200
