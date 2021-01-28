#!/usr/bin/python3
"""new view for User objects that handles
all default RestFul API actions"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_allUsers():
    """Retrieve a list of Users objects"""
    obj_dic = storage.all("User")
    return jsonify([users.to_dict() for users in obj_dic.values()])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieve a specific user object by id"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """Delete a specific user object by id"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a user object"""
    if request.get_json() is None:
        return "Not a JSON", 400
    elif 'email' not in request.get_json():
        return "Missing email", 400
    elif 'password' not in request.get_json():
        return "Missing password", 400
    else:
        user = User(**request.get_json())
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def uptade_user(user_id):
    """Update a user store into storage"""
    if request.get_json() is None:
        return "Not a JSON", 400
    user = storage.get(User, user_id)
    if user:
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        for key, value in request.get_json().items():
            if key not in ignore_keys:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)
