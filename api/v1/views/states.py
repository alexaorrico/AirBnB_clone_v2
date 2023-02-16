#!/usr/bin/python3
"""creates a new view for State Objects"""
from os import name
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models.state import State
from models import storage
import json


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """gets all state objects"""
    all_objects = storage.all(State)
    single_object = []
    for obj in all_objects.values():
        single_object.append(obj.to_dict())
    return jsonify(single_object)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_id(state_id):
    """gets the state object using his id"""
    all_objects = storage.get(State, state_id)
    if all_objects is None:
        abort(404)
    return jsonify(all_objects.to_dict()), 200


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """Deletes"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates"""
    res = request.get_json()
    if res is None:
        abort(400, {"Not a JSON"})
    if 'name' not in res:
        abort(400, {"Missing name"})
    obj = State(name=res['name'])
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_sate(state_id=None):
    """PUT"""
    res = request.get_json()
    if not res:
        abort(400, {"Not a JSON"})
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    i_key = ["id", "created_at", "updated_at"]
    for key, value in res.items():
        if key not in i_key:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
