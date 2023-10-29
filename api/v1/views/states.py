#!/usr/bin/python3
"""state view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """retrieve all states"""
    states_list = []
    for state in storage.all(State).values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def a_state(state_id):
    """retrieve a state with its id"""
    try:
        state = storage.get(State, state_id)
        return jsonify(state.to_dict())
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a State object"""
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def POST_request():
    """"post request"""
    data = request.get_json()
    if not data:
        return abort(400, {'message': 'Not a JSON'})
    if 'name' not in data:
        abort(400)
        return abort(400, {'message': 'Missing name'})
    # creation of a new state
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def PUT_state(state_id):
    """Put request"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
