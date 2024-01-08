#!/usr/bin/python3
"""User views for modules"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User



@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """Retrieves the list of all User objects"""
    user_list = storage.all(User).values()
    user_dict = []

    for user in user_list:
        user_dict.append(user.to_dict())

    return jsonify(user_dict)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a user based on it's ID"""
    user = storage.get(User, user_id)

    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a user based on it's ID"""
    user = storage.get(User, user_id)

    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """Adds a user"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """updates a user"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignore_list = ["id", "email", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in ignore_list:
            setattr(user, key, value)
        else:
            pass

    storage.save()
    return jsonify(user.to_dict()), 200
