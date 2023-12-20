#!/usr/bin/python3
"""users for API routes v1"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


# GET all users
# ============================================================================

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """get all users"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


# GET 1 user
# ============================================================================

@app_views.route('users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """get user by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


# DELETE a user
# ============================================================================

@app_views.route('users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """delete user by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


# CREATE a user
# ============================================================================

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """create new user"""
    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')

    if 'email' not in data:
        abort(400, 'Missing email')

    if 'password' not in data:
        abort(400, 'Missing password')

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


# UPDATE a user
# ============================================================================

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """updtae user by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    ignore_key = ['id', 'email', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_key:
            setattr(user, key, value)

    user.save()
    return jsonify(), 200
