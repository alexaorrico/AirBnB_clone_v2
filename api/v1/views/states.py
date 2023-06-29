#!/usr/bin/python3
'''Contains the State view for the API.'''
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """retrieves list of all the states"""
    state = storage.all(State)
    return jsonify([sts.to_dict() for sts in state.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state(state_id):
    """retrieves a the states"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """deletes a the states"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a State"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    obj = State(**request.get_json())
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update(state_id):
    """Updates a State object"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
