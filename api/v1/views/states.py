#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, jsonify, abort
from models import storage


@app_views.route('/states', strict_slashes=False)
def get_states():
    """ Return status of the APP as OK """
    states_list = []
    for state in storage.all('State').values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states_id(state_id):
    """ Return status of the APP as OK """
    for state in storage.all('State').values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_states_id(state_id):
    """ Return status of the APP as OK """
    for state in storage.all('State').values():
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
    abort(404)
