#!/usr/bin/python3
"""
This module contains a view for User object that handles all default
RESTful API actions(basically CRUD operations)
"""

from flask import abort, jsonify, request, make_response
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """ This method gets all instances of user """
    users_list = storage.all("User")
    all_users = []
    for obj in users_list.values():
        all_users.append(obj.to_dict())
    return jsonify(all_users)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user_by_id(user_id):
    """ This function gets a user by id """
    user = storage.get("User", user_id)
    if not user:
        abort(404, "Not found")
    return jsonify(user.to_dict())


@app_views.route(
    "/users/<user_id>", methods=["DELETE"], strict_slashes=False
)
def delete_user_by_id(user_id):
    """ This function deletes a user by id """
    user = storage.get("User", user_id)
    if not user:
        abort(404, "Not found")
    storage.delete(user)
    storage.save()
    return jsonify(user.to_dict()), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user_by_id():
    """ This function creates a new user """
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")
    if "email" not in new_user:
        abort(400, "Email is missing")
    if "password" not in new_user:
        abort(400, "Password is missing")
    user = User(**new_user)
    storage.new(user)
    storage.save()
    return make_response(user.to_dict(), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user_by_id(user_id):
    """ This function updates user by its id """
    user = storage.get("User", user_id)
    if not user:
        abort(404, "Not found")
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")
    ignore_list = ["id", "email", "created_at", "updated_at"]
    for key, value in new_user.items():
        if key not in ignore_list:
            setattr(user, key, value)
        user.save()
        storage.save()
    return jsonify(user.to_dict()), 200
