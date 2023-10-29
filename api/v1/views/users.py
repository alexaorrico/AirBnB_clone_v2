#!/usr/bin/python3
"""
Create a new view for User object that handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_ueers():
    """Get all user and display it as Json."""
    users = storage.all(User)
    list_users = []
    for user in users.values():
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Get user by id and display it as Json."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete user from storage."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create User"""
    user_data = request.get_json()
    if user_data is None:
        abort(400, 'Not a JSON')
    if 'email' not in user_data:
        abort(400, 'Missing email')
    if 'password' not in user_data:
        abort(400, 'Missing password')
    user = User(**user_data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def modify_user(user_id):
    """modify user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_data = request.get_json()
    if user_data is None:
        abort(400, 'Not a JSON')
    ignored_key = ['id', 'email', 'created_at', 'updated_at']
    for k, v in user_data.items():
        if k not in ignored_key:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200
