#!/usr/bin/python3
"""User"""
from flask import jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route("/users", methods=["GET"],
                 strict_slashes=False)
def get_users():
    """Gets the list of all users"""
    data = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(data)


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a user object"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def create_user():
    """Creates a user"""
    new_user_data = request.get_json()
    if not new_user_data:
        abort(400, "Not a JSON")
    if "email" not in new_user_data:
        abort(400, "Missing email")
    if "password" not in new_user_data:
        abort(400, "Missing password")
    new_user = User(**new_user_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data_to_update = request.get_json()
    for key, value in data_to_update.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(400)
