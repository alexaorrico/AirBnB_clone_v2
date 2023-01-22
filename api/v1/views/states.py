#!/usr/bin/python3
"""All objects"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.state import State
from flask import *


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def list_states():
    """list of states"""
    states = storage.all(State)
    return jsonify(
        [state.to_dict() for state in states.values()]
            )


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    """get metod for states"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(
        state.to_dict()
            )


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=True)
def delete_state(state_id):
    """Delete state method"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    return jsonify({}), 200)


@ app_views.route('/states', methods = ['POST'], strict_slashes = False)
def create_state():
    """create state"""
    get_json=request.get_json()
    if get_json is None:
        abort(404, 'Not a JSON')
    if get_json['name'] is None:
        abort(404, 'Missing Name')
    new_state=State(**get_json)
    new_state.save()
    return jsonify(new_state.to_dict()), 201)


@ app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updating state"""
    new_state=storage.get(State, state_id)
    if new_state is None:
        abort('404')
    if request.get_json() is None:
        abort('404', 'Not s JSON')
    update=request.get_json()
    for key, value in update.items():
        if key != 'id' or key != 'created_at' or key != 'updated_at':
            setattr(new_state, key, value)
    new_state.save()
    return jsonify(new_state.to_dict()), 200)
