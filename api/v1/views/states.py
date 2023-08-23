#!/usr/bin/python3
'''
Create a new view for State objects that handles all
default RESTFul API actions:
'''

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_state():
    state_list = []
    all_state = storage.all(State).values()
    for states in all_state:
        state_list.append(states.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def error_state(state_id):
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    return jsonify(states.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    states.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    rget_json = request.get_json()
    if rget_json is None:
        abort(400, 'Not a JSON')
    if 'name' not in rget_json:
        abort(400, 'Missing name')

    nstate = State(**rget_json)
    nstate.save()
    return jsonify(nstate.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    rget_json = request.get_json()
    if rget_json is None:
        abort(400, 'Not a JSON')

    for key, value in rget_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(states, key, value)
    states.save()
    return jsonify(states.to_dict()), 200
