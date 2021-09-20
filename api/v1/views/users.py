#!/usr/bin/python3
"""
User for API.
"""
from flask import abort, request, jsonify, make_response
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
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route(
    '/users/<user_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_user(user_id):
    """Deletes a user"""
    user = storage.get(User, user_id)
    if user:
        user.delete()
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route(
    '/users',
    methods=['POST'],
    strict_slashes=False)
def post_user():
    """Creates user"""
    all_user = request.get_json()
    if not all_user:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in all_user:
        return (jsonify({'error': 'Missing email'}), 400)
    if 'password' not in all_user:
        return (jsonify({'error': 'Missing password'}), 400)
    user = User(**all_user)
    user.save()
    return (jsonify(user.to_dict()), 201)


@app_views.route(
    '/users/<user_id>',
    methods=['PUT'],
    strict_slashes=False)
def put_user(user_id):
    """Updates a user """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
