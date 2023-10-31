#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""view for User object that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from datetime import datetime
import uuid

# get list of all users


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """get list of all users"""
    users = storage.all(User)
    users_list = []
    for user in users.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)

# get user by id


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """get user by id"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)

# delete user by id


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """delete user by id"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

# create user


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """create user"""
    user_json = request.get_json()
    if not user_json:
        abort(400, 'Not a JSON')
    if 'email' not in user_json:
        abort(400, 'Missing email')
    if 'password' not in user_json:
        abort(400, 'Missing password')
    user = User(**user_json)
    user.save()
    return jsonify(user.to_dict()), 201

# update user by id


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update user by id"""
    user_json = request.get_json()
    if not user_json:
        abort(400, 'Not a JSON')
    user = storage.get(User, user_id)
    if user:
        for key, value in user_json.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)
