#!/usr/bin/python3
"""
Handles RESTFul API actions for user
"""

from flask import abort
from api.v1.views import app_views
from flask import jsonify
from flask import request
from models.user import User
from models import storage


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def all_users():
    """
    Returns list of all users
    """
    users = storage.all("User")
    list_users = []
    for user in users.values():
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def one_user(user_id):
    """
    Returns a user object based on id
    """
    user = storage.get("User", user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a user object based on id
    """
    user = storage.get("User", user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def add_user():
    """
    Adds a user object based on data provided
    """
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")

    email = data['email']
    password = data['password']
    new_user = User(email=email, password=password)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates a user object based on data provided
    """
    user = storage.get("User", user_id)
    if user:
        data = request.get_json(silent=True)
        if not data:
            abort(400, "Not a JSON")
        keys_to_ignore = ["created_at", "email", "id", "updated_at"]
        for k, v in data.items():
            if k not in keys_to_ignore:
                setattr(user, k, v)
        storage.save()
        return jsonify(user.to_dict()), 200
    abort(404)
