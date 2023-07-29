#!/usr/bin/python3
"""user obj API"""
from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id=None):
    """Get all users or a users whose id is specified"""
    if user_id is None:
        users = storage.all(User).values()
        users_list = [user.to_dict() for user in users]
        return jsonify(users_list)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Create a new user"""
    user = request.get_json()
    if not user:
        abort(400, description="Not a JSON")
    if 'email' not in user:
        abort(400, description="Missing email")
    if 'password' not in user:
        abort(400, description="Missing password")
    obj = User(**user)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Update a user object"""
    user = storage.get(User, user_id)
    fixed_data = ['id', 'created_at', 'email', 'updated_at']
    if user is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in fixed_data:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
