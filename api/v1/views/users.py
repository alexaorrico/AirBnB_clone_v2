#!/usr/bin/python3
"""
The user module
"""
from models import storage
from flask import Blueprint, jsonify, request, abort
from models.user import User

users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')


@users_bp.route('/', methods=['GET'], strict_slashes=False)
def get_user():
    """
   function that gets the user from the storage
   """
    user = [users.to_dict() for users in storage.all(User).values()]
    return jsonify(user)


@users_bp.route('/<user_id>', methods=['GET'], strict_slashes=False)
def get_users(user_id):
    """
    function that gets the user from the storage
    """
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    return jsonify(users.to_dict())


@users_bp.route('/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_users(user_id):
    """
    function hat deletes the user from storage
    """
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    storage.delete(users)
    storage.save()
    return jsonify({})


@users_bp.route('/', methods=['POST'], strict_slashes=False)
def create_users():
    """
    function that creates the user
    """
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    if 'password' not in data:
        abort(400, description='Missing password')
    if 'email' not in data:
        abort(400, description='Missing email')
    new_users = User(**data)
    new_users.save()
    return jsonify(new_users.to_dict()), 201


@users_bp.route('/<user_id>', methods=['PUT'], strict_slashes=False)
def update_users(user_id):
    """
    function that updates new user
    """
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(users, key, value)
    users.save()
    return jsonify(users.to_dict())
