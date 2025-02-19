#!/usr/bin/python3
"""
Handles RESTful API actions for User objects
"""
from flask import jsonify, abort, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """
    Retrieves the list of all User objects
    """
    users = storage.all(User).values()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object by its ID
    """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object by its ID
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a new User object
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    data = request.get_json()
    if 'email' not in data:
        return abort(400, 'Missing email')
    if 'password' not in data:
        return abort(400, 'Missing password')
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object by its ID
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    user = storage.get(User, user_id)
    if user:
        data = request.get_json()
        ignore_keys = {'id', 'email', 'created_at', 'updated_at'}
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)
