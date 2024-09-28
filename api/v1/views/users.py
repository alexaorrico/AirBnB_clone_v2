#!/usr/bin/python3
"""
    This Module contains the api for the User
"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import abort, jsonify, request


@app_views.route('/users/<user_id>', strict_slashes=True, methods=['GET'])
@app_views.route('/users', strict_slashes=True, methods=['GET'])
def get_users(user_id=None):
    """This Method gets all the users

        Argument:
            user_id: the user id

        Returns: the one user if user_id is present or all if none is passed
    """
    if user_id:
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        return jsonify(user.to_dict()), 200
    users = [user.to_dict() for user in storage.all("User").values()]
    if not users:
        abort(404)
    return jsonify(users), 200


@app_views.route('/users/<user_id>', strict_slashes=True, methods=['DELETE'])
def delete_user(user_id):
    """This Method deletes the User instance"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    return jsonify({}), 200


@app_views.route('/users', strict_slashes=True, methods=['POST'])
def post_user():
    """This Method creates a new user"""
    if request.content_type != 'application/json':
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if "email" not in data.keys():
        return jsonify({"error": "Missing Email"}), 400
    if "password" not in data.keys():
        return jsonify({"error": "Missing Password"}), 400
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=True, methods=['PUT'])
def put_user(user_id):
    """This method updates the value of an instance of a user"""
    user = storage.get(User, user_id)
    if request.content_type != "application/json":
        return jsonify({"error": "Not a JSON"}), 400
    if not user:
        return abort(404)
    user.delete()
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "email",  "updated_at", "created_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
