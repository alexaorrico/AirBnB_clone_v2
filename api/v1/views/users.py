#!/usr/bin/python3
"""
Handles all default RestFul actions for user.
"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, jsonify, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_all_users():
    """Retrieves a list of all user objects"""
    users = []
    for user in storage.all('User').values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Returns a single user object based on user_id"""
    user = storage.get('User', user_id)
    if user is not None:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a user based on a given id"""
    user = storage.get('User', user_id)
    if user is not None:
        user.delete()
        storage.save()
    else:
        abort(404)
    return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a user with specified params"""
    req_dict = request.get_json()
    if req_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif 'email' not in req_dict:
        return (jsonify({'error': 'Missing email'}), 400)
    elif 'password' not in req_dict:
        return (jsonify({'error': 'Missing password'}), 400)
    user = User(**req_dict)
    user.save()
    return (jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates a user based on a  given user id"""
    req_dict = request.get_json()
    if req_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    user = storage.get('User', user_id)
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    if user is not None:
        for key in req_dict.keys():
            if key not in ignore_keys:
                setattr(user, key, req_dict[key])
        user.save()
        return (jsonify(user.to_dict()), 200)
