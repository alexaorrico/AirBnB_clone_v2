#!/usr/bin/python3
"""Create a new view for State objects that handles
all default RESTFul API actions"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_state.yml', methods=['GET'])
def get_states():
    dict_ = []
    for val in storage.all(State).values():
        dict_.append(val.to_dict())
    return jsonify(dict_)


@app_views.route('/states/<path:state_id>')
@swag_from('documentation/state/get_state.yml', methods=['GET'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<path:state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/state/delete_state.yml', methods=['DELETE'])
def delete_state(state_id):
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/state/post_state.yml', methods=['POST'])
def post_state():
    res = request.get_json()
    if type(res) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if 'name' not in res:
        return abort(400, {'message': 'Missing name'})
    new_state = State(**res)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<path:state_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/state/put_state.yml', methods=['PUT'])
def put_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in res.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
