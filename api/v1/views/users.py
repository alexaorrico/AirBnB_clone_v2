#!/usr/bin/python3
"""a module as users API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False)
def get_users():
    """a function to retrieve all users"""
    users = []
    all_users = storage.all("User").values()
    for user in all_users:
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route("/users/<user_id>")
def get_user(user_id):
    """a function to get a user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    """a function to delete a User object by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def post_user():
    """a function to create a new User object"""
    try:
        json_req = request.get_json()
    except Exception:
        json_req = None

    if not json_req:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in json_req:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in json_req:
        return jsonify({"error": "Missing password"}), 400

    user = User(**json_req)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'])
def update_user(user_id):
    """a function to update a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    try:
        json_req = request.get_json()
    except Exception:
        json_req = None

    if not json_req:
        return jsonify({"error": "Not a JSON"}), 400

    ignored_keys = ["id", "email", "created_at", "updated_at"]
    for key, value in json_req.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
