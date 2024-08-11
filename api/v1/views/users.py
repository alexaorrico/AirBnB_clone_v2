#!/usr/bin/python3
"""
Create a flask app that will serve the API, views module
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Return users
    """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Return user
    """
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Delete user
    """
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Create user
    """
    if request.content_type != 'application/json':
        return abort(400, "Not a JSON")
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    if 'email' not in data:
        return abort(400, "Missing email")
    if 'password' not in data:
        return abort(400, "Missing password")
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """
    Update user
    """
    if request.content_type != 'application/json':
        return abort(400, "Not a JSON")
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
