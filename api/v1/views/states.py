#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response
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
    catch_state = storage.get('State', state_id)
    if catch_state is None:
        abort(404)
    else:
        storage.delete(catch_state)
        storage.save()
        return make_response(jsonify({}), 200)
