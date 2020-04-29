#!/usr/bin/python3
"""User module"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, request, abort


@app_views.route("/users", methods=["GET"])
def get_users():
    """Gets user objects"""
    users_list = []
    for i in storage.all(User).values():
        users_list.append(i.to_dict())
    return jsonify(users_list)


@app_views.route("/users/<users_id>", methods=["GET"])
def get_users_id(users_id):
    """Gets a certain user based on the user id"""
    if storage.get(User, users_id) is None:
        abort(404)
    else:
        return (jsonify(storage.get(User, users_id).to_dict()))


@app_views.route("/users/<users_id>", methods=["DELETE"])
def delete_users(users_id):
    """Deletes a user based on id"""
    all_the_users = storage.get(User, users_id)
    if all_the_users is None:
        abort(404)
    storage.delete(all_the_users)
    storage.save()
    return (jsonify({})), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """Creates a new user object"""
    data = request.get_json()
    if not data:
        return (jsonify({"error": "Not a JSON"})), 400
    if "email" not in data:
        return (jsonify({"error": "Missing email"})), 400
    if "password" not in data:
        return (jsonify({"error": "Missing password"})), 400
    new_user_obj = User(**data)
    new_user_obj.save()
    return (new_user_obj.to_dict()), 201


@app_views.route("/users/<users_id>", methods=["PUT"], strict_slashes=False)
def update_users(users_id):
    """Updates the users object"""
    data = request.get_json()
    all_the_users = storage.get(User, users_id)
    if all_the_users is None:
        abort(404)
    if not data:
        return (jsonify({"error": "Not a JSON"})), 400
    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(all_the_users, key, value)
    storage.save()
    return (jsonify(all_the_users.to_dict())), 200
