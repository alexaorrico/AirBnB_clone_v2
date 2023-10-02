#!/usr/bin/python3
"""
This Module contains User object that handles
all default RESTFul API actions
"""
from flask import Flask, request, abort, jsonify, make_response
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """retrieves a list of all users"""
    users_obj = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(users_obj)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """retrieve a user based on its ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes a user based on its ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """creates a new user objcet"""
    json_request = request.get_json()
    if not json_request:
        abort(400, "Not a JSON")
    required_keys = ['email', 'password']
    if required_keys[0] not in json_request:
        abort(400, "Missing email")
    if required_keys[1] not in json_request:
        abort(400, "Missing password")
    user = User(**json_request)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """updates a user based on its ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    json_request = request.get_json()
    if not json_request:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in json_request.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
