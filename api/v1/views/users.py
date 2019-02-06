#!/usr/bin/python3
""" module that handles all default RestFul API actions
"""

from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/users", strict_slashes=False)
def get_users():
    """ get all user objects """
    objs = storage.all("User")
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route("/users/<user_id>", strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """ get user object """
    obj = storage.get("User", user_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/users/<user_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """delete user object"""
    obj = storage.get("User", user_id)
    if obj:
        obj.delete()
        return jsonify({}), 200
    abort(404)


@app_views.route("/users", strict_slashes=False, methods=['POST'])
def post_user():
    """create user instance"""
    request_dict = request.get_json()
    if not request_dict:
        abort(400, jsonify({'message': 'Not a JSON'}))
    if 'email' not in request_dict:
        abort(400, jsonify({'message': 'Missing email'}))
    if 'password' not in request_dict:
        abort(400, jsonify({'message': 'Missing password'}))
    obj = User(**request_dict)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False, methods=['PUT'])
def put_user(user_id):
    """update user object"""
    obj = storage.get("User", user_id)
    if not obj:
        abort(404)
    request_dict = request.get_json()
    if not request_dict:
        abort(400, jsonify({'message': 'Not a JSON'}))
    for key, value in request_dict.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    return jsonify(obj.to_dict()), 200
