#!/usr/bin/python3
"""
A new view for state objects that handles all RESTFul api
"""
from flask import Flask, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def all_states():
    """
    get the list list of all state objects
    """
    states = storage.all('State')
    s_list = []
    for state in states.values():
        s_list.append(state.to_dict())
    return jsonify(s_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_a_state(state_id):
    states = storage.all('State')
    for state in states.values():
        if state.id == state_id:
            state = state.to_dict()
            return jsonify(state)
    abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_a_state(state_id):
    """deletes a state objects"""
    state = storage.get(classes['State'], state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})
