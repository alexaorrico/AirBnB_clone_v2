#!/usr/bin/python3
"""User views for API"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    """Return users list in format JSON"""
    users = storage.all(User)
    lis_user = []
    for user in users.values():
        lis_user.append(user.to_dict())
    return jsonify(lis_user)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Return a specific User object"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete user id"""
    users = storage.all(User)
    for user in users.values():
        if user.id == user_id:
            storage.delete(user)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if "email" not in data:
        abort(400, 'Missing email')
    if "password" not in data:
        abort(400, 'Missing password')
    new_user = User(**data)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update given User"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
