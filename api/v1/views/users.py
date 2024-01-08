#!/usr/bin/python3
""" module view for user objects;
handles all default Restful API actions
"""
from flask import Flask, jsonify, request, abort
from models import storage
from models.user import User
from . import app_views
import uuid


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """gets list of all state objects"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id=None):
    """get user by id"""

    # print("Full request: ", request)
    user = storage.get(User, user_id)
    # print('State id is {}'.format(state_id))
    # print('State id is type {}'.format(type(state_id)))
    # print('State is {}'.format(state))

    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """deletes a state identified by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """create state from http request"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')

    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """updates a state"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, val in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, val)
    user.save()
    return jsonify(user.to_dict()), 200
