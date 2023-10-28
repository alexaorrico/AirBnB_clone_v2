#!/usr/bin/python3
"""handles all defaults RESTful API actions for states"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """retrieve all users"""
    users = storage.all(User)
    users_list = []

    for user in users.values():
        users_list.append(user.to_dict())

    return jsonify(users_list)


@app_views.route('users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """retrieves a state based on its id"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    return abort(404)


@app_views.route('users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """deletes a user based on its id"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates a new user"""
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    if "email" not in data:
        return abort(400, "Missing email")
    if "password" not in data:
        return abort(400, "Missing password")
    user = User()
    user.email = data["email"]
    user.password = data["password"]
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """updates a given user"""
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
