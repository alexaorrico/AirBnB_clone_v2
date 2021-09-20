#!/usr/bin/python3
"""creates a new view for State Objects"""
from os import name
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models.user import User
from models import storage
import json


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user():
    """gets all state objects"""
    all_objects = storage.all(User)
    single_object = []
    for obj in all_objects.values():
        single_object.append(obj.to_dict())
    return jsonify(single_object)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_uer_id(user_id):
    """gets the state object using his id"""
    all_objects = storage.get(User, user_id)
    if all_objects is None:
        abort(404)
    return jsonify(all_objects.to_dict()), 200


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):
    """Deletes"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates"""
    result = request.get_json()
    if not result:
        abort(400, {"Not a JSON"})
    if 'email' not in result:
        abort(400, {"Missing email"})
    if 'password' not in result:
        abort(400, {"Missing password"})
    obj = User()
    for key, value in result.items():
        setattr(obj, key, value)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id=None):
    """PUT"""
    res = request.get_json()
    if not res:
        abort(400, {"Not a JSON"})
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    i_key = ["id", "created_at", "updated_at"]
    for key, value in res.items():
        if key not in i_key:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
