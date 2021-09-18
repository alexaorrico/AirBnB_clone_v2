#!/usr/bin/python3
"""creates a new view for State Objects"""
from os import name
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage
import json

@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """gets all state objects"""
    if request.method == 'GET':
        all_objects = storage.all(State)
        single_object = []
        for key, value in all_objects.items():
            single_object.append(value.to_dict)
        return jsonify(single_object)

@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_state_id(state_id):
    """gets the state object using his id"""
    if request.method == 'GET':
        all_objects = storage.all(State)
        new_dict = {}
        for key, value in all_objects.items():
            if state_id == value.id:
                new_dict = value.to_dict
                return jsonify(new_dict)
        abort(404)




@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete(state_id=None):
    """Deletes"""
    obj = storage.get('State', state_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post():
    """Creates"""
    res = request.get_json()
    if not res:
        abort(400, {"Not a JSON"})
    if 'name' not in res:
        abort(400, {"Missing name"})
    obj = State(name=res['name'])
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201

@app_views.route('/states', methods=['PUT'], strict_slashes=False)
def post():
    """PUT"""
    res = request.get_json()
    if not res:
        abort(400, {"Not a JSON"})
    obj = storage.get('State', state_id)
    if obj is None:
        abort(404)
    i_key = ["id", "created_at", "updated_at"]
    for key, value in res.items():
        if key not in i_key:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
