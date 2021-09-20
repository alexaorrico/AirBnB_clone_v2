#!/usr/bin/python3
"""
User for API.
"""

from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route(
    '/users',
    methods=['GET'],
    strict_slashes=False)
def get_users():
    """Returns all user in jason format"""
    users = []
    for user in storage.all('User').values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route(
    '/users/<user_id>',
    methods=['GET'],
    strict_slashes=False)
def get_id_user(user_id):
    """Returns id user in json format"""
    user = storage.get('User', user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route(
    '/users/<user_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_user(user_id):
    """Deletes a user"""
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
    """Creates user"""
    all_user = request.get_json()
    if not all_user:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif 'email' not in all_user:
        return (jsonify({'error': 'Missing email'}), 400)
    elif 'password' not in all_user:
        return (jsonify({'error': 'Missing password'}), 400)
    user = User(**all_user)
    user.save()
    return (jsonify(user.to_dict()), 201)


@app_views.route(
    '/users/<user_id>',
    methods=['PUT'],
    strict_slashes=False)
def put_user(user_id):
    """Updates a user with a given id"""
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    all_user = request.get_json()
    if not all_user:
        return (jsonify({'error': 'Not a JSON'}), 400)
    user = storage.get('User', city_id)
    if user:
        for key in all_user.keys():
            if key not in ignore_keys:
                setattr(user, key, all_user[key])
        user.save()
        return (jsonify(user.to_dict()), 200)