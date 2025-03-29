#!/usr/bin/python3
"""Users view"""


from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieve all users"""
    users = storage.all(User)
    users_dict = [user.to_dict() for user in users.values()]
    return jsonify(users_dict)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieve a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes aA User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a User"""
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    if 'email' not in payload:
        abort(400, "Missing email")
    if 'password' not in payload:
        abort(400, "Missing password")
    user = User(**payload)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    update_data = request.get_json()
    if not update_data:
        abort(400, "Not a JSON")
    for key, value in update_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
