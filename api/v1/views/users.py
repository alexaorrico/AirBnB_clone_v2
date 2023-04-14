#!/usr/bin/python3
"""Defines the RESTful API actions for the user objects."""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects."""
    amenities = storage.all(User).values()
    return jsonify([user.to_dict() for user in amenities])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_users_id(user_id):
    """retrieve a User object"""
    users = storage.all(User)
    for key, value in users.items():
        if users[key].id == user_id:
            return value.to_dict()
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}, 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a user object"""
    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')

    if 'email' not in body:
        abort(400, 'Missing email')
    if 'password' not in body:
        abort(400, 'Missing password')
    user = User(**body)
    storage.new(user)
    storage.save()
    return (jsonify(user.to_dict()), 201)


@app_views.route('users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a user object."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return (jsonify(user.to_dict()), 200)
