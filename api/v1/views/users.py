#!/usr/bin/python3
"""
Defines User endpoints
"""
from models import storage
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_all_users():
    """Gets all Users."""
    users_dict = storage.all("User")
    return jsonify([user.to_dict() for user in users_dict.values()])


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """Gets an User by id."""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return user.to_dict()


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """Deletes an User."""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return {}, 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def post_users():
    """Creates an User."""
    json_data = request.get_json()
    if json_data is None:
        return "Not a JSON", 400
    if "email" not in json_data:
        return "Missing email", 400
    if "password" not in json_data:
        return "Missing password", 400
    new_user = User(**json_data)
    new_user.save()
    return new_user.to_dict(), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """Updates an User."""
    ignore = ["id", "created_at", "updated_at"]
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        return "Not a JSON", 400
    for key, value in json_data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return user.to_dict(), 200
