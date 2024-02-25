#!/usr/bin/python3
"""Defines all routes for the `User` entity
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage, classes


@app_views.route("/users", methods=["GET"])
def get_users():
    """Returns all users in json response"""
    users = []
    users_objs = storage.all("User")
    for user in users_objs.values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route("/users/", methods=["POST"])
def create_user():
    """Creates a new user in storage"""
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, description="Not a JSON")
    if "email" not in data:
        return abort(400, description="Missing email")
    if "password" not in data:
        return abort(400, description="Missing password")
    user = classes["User"](**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Returns a user object or None if not found."""
    user = storage.get("User", user_id)
    return jsonify(user.to_dict()) if user else abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Deletes a user object from storage"""
    user = storage.get("User", user_id)
    if user is None:
        return abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """Update a user object by id"""
    user = storage.get("User", user_id)
    if user is None:
        return abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, description="Not a JSON")

    data.pop("id", None)
    data.pop("email", None)
    data.pop("updated_at", None)
    data.pop("created_at", None)

    for k, v in data.items():
        setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict())
