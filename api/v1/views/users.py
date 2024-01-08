#!/usr/bin/python3
"""
a new view for User objects that handles all default RESTFul API actions.
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def get_user_or_update_user(user_id):
    """
    Retrieves, updates, or deletes a User object by ID.

    GET /api/v1/users/<user_id> - Retrieves a User object.
    PUT /api/v1/users/<user_id> - Updates a User object.
    DELETE /api/v1/users/<user_id> - Deletes a User object.

    Args:
    user_id (str): ID of the User.

    Returns:
    JSON: User obj or success message.
    """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'PUT':
        try:
            data = request.get_json()
        except Exception:
            abort(400, 'Not a JSON')

        if data is None:
            abort(400, 'Not a JSON')

        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['GET', 'POST'])
def get_users_or_create_user():
    """
    Retrieves the list of all User objects or creates a new User.

    GET /api/v1/users - Retrieves the list of all User objects.
    POST /api/v1/users - Creates a new User.

    Returns:
    JSON: List of User objects or newly created User.
    """
    if request.method == 'GET':
        users = storage.all(User).values()
        return jsonify([user.to_dict() for user in users])

    if request.method == 'POST':
        try:
            data = request.get_json()
        except Exception:
            abort(400, 'Not a JSON')

        if data is None:
            abort(400, 'Not a JSON')

        if 'email' not in data:
            abort(400, 'Missing email')

        if 'password' not in data:
            abort(400, 'Missing password')

        new_user = User(**data)
        new_user.save()
        return jsonify(new_user.to_dict()), 200
