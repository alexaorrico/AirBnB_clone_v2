#!/usr/bin/python3
"""Handles all RESTful API actions for User objects"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User
from hashlib import md5


@app_views.route("/users", methods=["GET"])
def users():
    """Retrieve the list of all User objects"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Retrieve a User object by ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a User object by ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"])
def create_user():
    """Create a new User object"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """Update a User object by ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    ignored_keys = ["id", "email", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_keys:
            if key == "password":
                value = md5(str(value).encode()).hexdigest()
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
