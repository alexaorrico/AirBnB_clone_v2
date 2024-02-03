#!/usr/bin/python3
"""User RESTAPI"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route("/users", strict_slashes=False)
def get_users():  # Get all users
    users = storage.all(User)
    return jsonify([value.to_dict() for _, value in users.items()])


@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user(user_id):  # get a specific user
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route("/users/<string:user_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_user(user_id):  # Delete a user
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():  # Create a user
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")
    new_user = User(**data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<string:user_id>",
                 strict_slashes=False, methods=["PUT"])
def update_user(user_id):  # Update a user
    user = storage.get(User, user_id)
    if user:
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at", "email"]:
                setattr(user, key, value)
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
    abort(404)
