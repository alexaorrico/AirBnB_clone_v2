#!/usr/bin/python3
"""Users API views"""
from flask import jsonify, abort, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_users():
    """Retrieves a list of all User objects"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a specific User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a specific User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new User"""
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(**data)
    storage.new(new_user)

    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
