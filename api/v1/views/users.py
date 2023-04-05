#!/usr/bin/python3
"""
Defines the User view.
"""

from flask import Blueprint, jsonify, request
from models.user import User


user_view = Blueprint('user_view', __name__, url_prefix='/api/v1/users')


@user_view.route('', methods=['GET'])
def get_users():
    """
    Retrieves a list of all User objects.
    """
    users = User.query.all()
    users_json = [user.to_dict() for user in users]
    return jsonify(users_json)


@user_view.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieves a User object with the specified user_id.
    """
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())


@user_view.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes the User object with the specified user_id.
    """
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    user.delete()
    return jsonify({}), 200


@user_view.route('', methods=['POST'])
def create_user():
    """
    Creates a new User object.
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in data:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in data:
        return jsonify({'error': 'Missing password'}), 400
    user = User.create(**data)
    return jsonify(user.to_dict()), 201


@user_view.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates the User object with the specified user_id.
    """
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in data.items():
        if key not in ('id', 'email', 'created_at', 'updated_at'):
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
