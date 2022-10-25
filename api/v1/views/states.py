#!/usr/bin/python3
""" views for the State resource """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_states(state_id=None):
    """ An endpoint that returns all states or a specific state """
    if state_id:
        all_states = storage.all('State')
        state_id = "State.{}".format(state_id)
        if state_id in all_states:
            state = all_states[state_id]
            return jsonify(state.to_dict()), 200
        else:
            abort(404)
    else:
        rlist = []
        all_states = storage.all('State')
        for state in all_states.values():
            rlist.append(state.to_dict())
        return jsonify(rlist)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """ An endpoint that deletes a specific state """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False,
                 methods=['POST'])
def create_state():
    """ An endpoint that creates a state """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if 'name' not in content:
        abort(400, 'Missing name')
    new_state = State(name=content['name'])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['PUT'])
def modify_state(state_id):
    """ An endpoint that modifies a state """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    for k, v in content.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict()), 200
