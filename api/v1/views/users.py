#!/usr/bin/python3
"""Flask application for Users class/entity"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def retrieves_all_users():
    """Retrieves the list of all User"""
    users = storage.all(User).values()
    users_list = []
    for user in users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    users = storage.get(User, user_id)
    if not users:
        abort(404)
    return jsonify(users.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def deletes_users(user_id):
    """Deletes a User object"""
    users = storage.get(User, user_id)
    if not users:
        abort(404)
    storage.delete(users)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def creates_users():
    """Creates a User"""
    user_data = request.get_json()
    if not user_data:
        abort(400, "Not a JSON")
    elif "email" not in user_data:
        abort(400, "Missing email")
    elif "password" not in user_data:
        abort(400, "Missing password")

    new_users = User(**new_users)
    new_users.save()
    return jsonify(new_users.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_users(user_id):
    """Updates a User object"""
    user_data = request.get_json()
    users = storage.get(User, user_id)
    if not user_data:
        abort(400, "Not a JSON")
    for key, value in user_data.items():
        if key is not ["id", "email", "created_at", "updated_at"]:
            setattr(users, key, value)
    storage.save()
    return jsonify(users.to_dict()), 200
