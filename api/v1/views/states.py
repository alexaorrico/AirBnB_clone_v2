#!/usr/bin/python3
"""
States file for APi project
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def list_states():
    """lists all states"""
    s_list = []
    states = storage.all("State")
    for state in states.values():
        s_list.append(state.to_dict())
    return jsonify(s_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def GetStateById(state_id):
    """Retrieves state based on its id for GET HTTP method"""
    all_states = storage.all("State")
    for state in all_states.values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def DeleteStateById(state_id):
    """Deletes an state based on its id for DELETE HTTP method"""
    states = storage.all('State')
    s_id = "State." + state_id
    to_del = states.get(s_id)
    if to_del is None:
        abort(404)
    storage.delete(to_del)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def PostState():
    """Posts a state"""
    info = request.get_json()
    if not info:
        abort(400, 'Not a JSON')
    elif "name" not in info:
        abort(400, 'Missing name')
    state = State()
    state.name = info['name']
    state.save()
    state = state.to_dict()
    return jsonify(state), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def PutState(state_id):
    """ Updates a State uses PUT HTTP method"""
    exists = False
    all_states = storage.all("State")
    for state in all_states.values():
        print(state.name, state.id)
        if state.id == state_id:
            exists = True
    if not exists:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, 'Not a JSON')
    upt_state = all_states['{}.{}'.format('State', state_id)]
    upt_state.name = info['name']
    upt_state.save()
    upt_state = upt_state.to_dict()
    return jsonify(upt_state), 201


if __name__ == '__main__':
    pass
