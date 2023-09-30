#!/usr/bin/python3
"""Handles all RESTful API actions for `User`"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User
from hashlib import md5


@app_views.route("/users")
def users():
    """Get all users

    Returns:
        list: All the users
    """
    users = storage.all(User)
    result = []

    for user in users.values():
        result.append(user.to_dict())

    return jsonify(result)


@app_views.route("/users/<user_id>")
def one_user(user_id):
    """Get one user

    Args:
        user_id (str): ID of the user

    Returns:
        dict: The user in JSON
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete user

    Args:
        user_id (str): ID of the user

    Returns:
        dict: Am empty JSON
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    user.delete()
    storage.save()

    return jsonify({})


@app_views.route("/users", methods=["POST"])
def create_user():
    """Create user

    Returns:
        dict: User JSON
    """
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    if "email" not in payload:
        abort(400, "Missing email")
    if "password" not in payload:
        abort(400, "Missing password")

    user = User(**payload)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """Update user

    Args:
        user_id (str): ID of the user

    Returns:
        dict: Updated user in JSON
    """
    user = storage.get(User, user_id)
    payload = request.get_json()
    if not user:
        abort(404)
    if not payload:
        abort(400, description="Not a JSON")

    for key, value in user.to_dict().items():
        if key not in ["id", "email", "created_at", "updated_at", "__class__"]:
            if key in payload:
                if key == "password":
                    setattr(user, key,
                            md5(str(payload[key]).encode()).hexdigest())
                else:
                    setattr(user, key,
                            payload[key] if key in payload else value)
    user.save()

    return jsonify(user.to_dict())
