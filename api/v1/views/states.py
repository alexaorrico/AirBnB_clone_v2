#!/usr/bin/python3
'''
state blueprint
'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import State, storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    '''
    gets list of states
    '''
    if state_id is None:
        state = storage.all('State')
        states = [value.to_dict() for key, value in state.items()]
        return jsonify(states)
    states = storage.get('State', state_id)
    if states is not None:
        return jsonify(states.to_dict())
    abort(404)

@app_views.route('/states/<s_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(s_id):
    '''
    deletes state based off id
    '''
    state_d = storage.get('State', s_id)
    if state_d is None:
        abort(404)
    storage.delete(state_d)
    storage.save()
    return (jsonify({}))
    