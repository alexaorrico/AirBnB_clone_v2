#!/usr/bin/python3
"""
User view for API.

"""

from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route(
    '/users',
    methods=['GET'],
    strict_slashes=False)
def get_all_users():
    """Returns JSON of all users"""
    users = []
    for user in storage.all('User').values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route(
    '/users/<user_id>',
    methods=['GET'],
    strict_slashes=False)
def get_user(user_id):
    """Returns JSON user with a given id"""
    user = storage.get('User', user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route(
    '/users/<user_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_user(user_id):
    """Deletes a user with a given id"""
    user = storage.get('User', user_id)
    if user:
        user.delete()
        storage.save()
    return (jsonify({}), 200)


@app_views.route(
    '/users',
    methods=['POST'],
    strict_slashes=False)
def post_user():
    """Creates a user"""
    user_dict = request.get_json()
    if not user_dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif 'email' not in user_dict:
        return (jsonify({'error': 'Missing email'}), 400)
    elif 'password' not in user_dict:
        return (jsonify({'error': 'Missing password'}), 400)
    user = User(**user_dict)
    user.save()
    return (jsonify(user.to_dict()), 201)


@app_views.route(
    '/users/<user_id>',
    methods=['PUT'],
    strict_slashes=False)
def put_user(user_id):
    """Updates a user with a given id"""
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    user_dict = request.get_json()
    if not user_dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    user = storage.get('User', city_id)
    if user:
        for key in user_dict.keys():
            if key not in ignore_keys:
                setattr(user, key, user_dict[key])
        user.save()
        return (jsonify(user.to_dict()), 200)
