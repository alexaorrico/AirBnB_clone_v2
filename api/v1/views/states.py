#!/usr/bin/python3
"""Create a new view for State objects that handles all"""
from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False, methods=['GET'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_states(state_id=None):
    if state_id:
        all_states = storage.all('State')
        state_id = "State.{}".format(state_id)
        if state_id in all_states:
            state = all_states[state_id]
            return jsonify(state.to_dict()), 200
        else:
            abort(404)
    else:
        stateslist = []
        all_states = storage.all('State')
        for state in all_states.values():
            stateslist.append(state.to_dict())
        return jsonify(stateslist)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_state(state_id):
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False,
                 methods=['POST'])
def pos_state():
    res = request.get_json()
    if res is None:
        abort(400, 'Not a JSON')
    if 'name' not in res:
        abort(400, 'Missing name')
    newState = State(name=res['name'])
    storage.new(newState)
    storage.save()
    return jsonify(newState.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['PUT'])
def put_state(state_id):
    res = request.get_json()
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if res is None:
        abort(400, 'Not a JSON')
    for k, v in res.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict()), 200
