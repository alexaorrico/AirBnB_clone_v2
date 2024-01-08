#!/usr/bin/python3
"""Create a new view for User object that
handles all default RESTFul API actions"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route("/users", methods=["GET"],
                 strict_slashes=False)
def users():
    """get all users objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users]), 200


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user(user_id):
    """method to get user id"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    return jsonify(user.to_dict()), 200


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """method to delete user"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def create_user():
    """method to create a new user"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")
    user = User(**data)
    storage.new(user)
    storage.save()

    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """Method to update a user"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, val in data.items():
        if key in ["id", "email", "created_at", "updated_at"]:
            continue
        setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
