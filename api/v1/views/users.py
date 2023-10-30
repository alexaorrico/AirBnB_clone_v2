#!/usr/bin/python3
"""
 view for User objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects
    """
    all_users = storage.all(User).values()
    users_serializable = []
    for user in all_users:
        users_serializable.append(user.to_dict())
    return jsonify(users_serializable)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    A method to delete a user
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    A method to create new user
    """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if 'email' not in content:
        abort(400, 'Missing email')
    if 'password' not in content:
        abort(400, 'Missing password')
    user = User(**content)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """
    A method to update an existing user
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    skip = ['id', 'email', 'created_at', 'updated_at']
    for key, value in content.items():
        if key not in skip:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
