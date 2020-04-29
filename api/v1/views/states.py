#!/usr/bin/python3
"""Create a new view for State objects that handles all default RestFul API"""


from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states(state_id=None):
    """view for State objects that handles all default RestFul API actions"""
    all_states = storage.all('State')
    if state_id:
        state_id = "State.{}".format(state_id)
        if state_id in all_states:
            state = all_states[state_id]
            return jsonify(state.to_dict()), 200
        else:
            abort(404)
    else:
        stateList = []
        for state in all_states.values():
            stateList.append(state.to_dict())
        return jsonify(stateList)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def states_delete(state_id=None):
    """Deletes a State object:: DELETE /api/v1/states/state_id"""
    id_state = storage.get('State', state_id)
    if state_id is None:
        abort(404)
    else:
        storage.delete(id_state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def states_create():
    """Creates new states"""
    res = request.get_json()
    if res is None:
        abort(400, "Not a JSON")
    if 'name' not in res:
        abort(400, "Missing name")
    newState = State(name=res['name'])
    storage.new(newState)
    storage.save()
    return jsonify(newState.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def states_put(state_id=None):
    """updates a value from an instance"""
    state = storage.get('State', state_id)
    res = request.get_json()

    if res is None:
        abort(400, "Not a JSON")
    if state is None:
        abort(404)
    for k, v in res.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict()), 200
