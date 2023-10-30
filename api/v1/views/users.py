#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, request
from models import storage, user


@app_views('/users', methods=['GET'], strict_slashes=False)
def users():
    """Retrieves the list of all User objects"""
    users = storage.all(user).values()
    users_list = []
    for user in users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user(user_id):
    """Retrieves a user object"""
    user = storage.get(user, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user.to_dict()), 200


@app_views('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes user object"""
    user = storage.get(user, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates user object"""
    if not request.get_json():
        return jsonify({"error": "Not a Json"}), 400
    if 'email' not in request.get_json():
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.get_json():
        return jsonify({"error": "Missing password"}), 400
    user = user(**request.get_json())
    user.save()
    return jsonify(user.to_dict()), 201


@app_views('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """updates user object"""
    user = storage.get(user, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    if not request.get_json():
        return jsonify({"error": "Not a Json"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
