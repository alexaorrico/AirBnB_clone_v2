#!/usr/bin/python3
"""
Creates views for State objects
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves all state objects"""
    data = []
    for val in storage.all(State).values():
        data.append(val.to_dict())
    return jsonify(data)


@app_views.route('/states/<path:state_id>')
def get_state(state_id):
    """Retrieves a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<path:state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a state object"""
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    state.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a State"""
    res = request.get_json()
    if type(res) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if 'name' not in res:
        return abort(400, {'message': 'Missing name'})

    new_state = State(**res)
    new_state.save()
    return jsonify(new_state.to_dict())


@app_views.route('/states/<path:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """Updates a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for k, v in res.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict()), 200
