#!/usr/bin/python3
"""New Funtion states"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ss"""
    list_dict = []
    for obj in storage.all(State).values():
        list_dict.append(obj.to_dict())
    return jsonify(list_dict), 200


@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """ddd"""
    obj = storage.get(State, state_id)
    if (obj):
        return jsonify(obj.to_dict()), 200
    else:
        return jsonify({"error": "Not found"}), 404


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state_by_id(state_id):
    """delete method api"""
    obj = storage.get(State, state_id)
    if (obj):
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        return jsonify({"error": "Not found"}), 404


@app_views.route('/states/<state_id>', methods=['POST'], strict_slashes=False)
def post_state_create(state_id):
    """ddd"""
    a = State()
    a.name = "jose"
    storage.new(a)
    storage.save()
    return jsonify(a.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['POST'], strict_slashes=False)
def put_state_update(state_id):
    """ddd"""
    pass
