#!/usr/bin/python3
"""module to handle api request on user"""
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    """method to get all users"""
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """method to get a user by id"""
    for user in storage.all(User).values():
        if user.id == user_id:
            return jsonify(user.to_dict())
    abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """method to delete user"""
    for user in storage.all(User).values():
        if user.id == user_id:
            user.delete()
            storage.save()
            return make_response(jsonify(user.to_dict), 200)
    abort(404)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    """method to create user"""
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, "Not a JSON")
    if 'email' not in request_data.keys():
        abort(400, "Missing email")
    if 'password' not in request_data.keys():
        abort(400, "Missing password")
    new_user = User(**request_data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """method to update user"""
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, "Not a JSON")
    for user in storage.all(User).values():
        if user.id == user_id:
            for attrib, value in request_data.items():
                if attrib in ["id", "email", "created_at", "updated_at"]:
                    continue
                setattr(user, attrib, value)
            user.save()
            return make_response(jsonify(user.to_dict()), 200)
    abort(404)
