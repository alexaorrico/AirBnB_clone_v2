#!/usr/bin/python3
""" module: 'users.py'
        create route for users
"""

from flask import jsonify
from flask import abort
from flask import request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users")
def get_users():
    """retrieves all users """
    users = []
    users_obj = storage.all(User)
    for user_obj in users_obj.values():
        users.append(user_obj.to_dict())

    return jsonify(users), 200


@app_views.route("/users/<string:user_id>")
def get_user(user_id=None):
    """retrieves a specific user """
    if user_id is None:
        abort(404)

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", methods=['DELETE'])
def delete_user(user_id=None):
    """Delete a specific user """
    if user_id is None:
        abort(404)

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return {}, 200


@app_views.route("/users/", methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a new user"""
    user_dict = None
    try:
        user_dict = request.get_json()
        if not isinstance(user_dict, dict):
            raise ValueError
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in user_dict:
        return jsonify({"error": "Missing name"}), 400
    if 'password' not in user_dict:
        return jsonify({"error": "Missing password"}), 400

    user = User()
    for key, val in user_dict.items():
        setattr(user, key, val)

    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id=None):
    """ updates a user object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_dict = None
    try:
        user_dict = request.get_json()
        if not isinstance(user_dict, dict):
            raise ValueError
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    for key, val in user_dict.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, val)

    storage.save()
    return jsonify(user.to_dict()), 200
