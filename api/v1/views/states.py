#!/usr/bin/python3
"""State route"""
import json

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False)
def get_states():
    """Endpoint to retreive all states"""
    list_states = []
    objs = storage.all(State).values()
    for v in objs:
        v = v.to_dict()
        list_states.append(v)
    return jsonify(list_states)


@app_views.route('/states/<string:state_id>', strict_slashes=False)
def get_state_by_id(state_id):
    """Endpoint to retreive an object by id"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/states/<string:state_id>',
                 methods=['GET', 'DELETE'], strict_slashes=False)
def delete_obj(state_id):
    """Endpoint to delete an object"""
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def add_new_obj():
    """Endpoint to add new objects"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>',
                 methods=['PUT', 'GET'], strict_slashes=False)
def update_obj(state_id):
    """Endpoint to update an obj"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict()), 200
