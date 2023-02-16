#!/usr/bin/python3

"""users view module"""

from api.v1.views import app_views
from models.user import User
from flask import jsonify, abort, request
import models


@app_views.route('/users', methods=["GET"], strict_slashes=False)
def users():
    """return all the users"""
    all_users = models.storage.all(User)
    return jsonify([user.to_dict() for user in all_users.values()])


@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
def get_user_by_id(user_id):
    """return a by id or 404"""
    user = models.storage.get(User, user_id)
    if user_id is None:
        return abort(404)
    if user is None:
        return abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route("/users/<user_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """delete user data by id"""
    user = models.storage.get(User, user_id)
    if user_id is None:
        return abort(404)
    if user is None:
        return abort(404)
    else:
        models.storage.delete(user)
        return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def add_user():
    """add new user"""
    try:
        req_data = request.get_json(force=True)
    except Exception:
        req_data = None

    if req_data is None:
        return "Not a JSON", 400

    if "email" not in req_data.keys():
        return "Missing email", 400
    if  "password" not in req_data.keys():
        return "Missing password", 400

    new_user = User(req_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """update user object"""
    try:
        req_data = request.get_json(force=True)
    except Exception:
        return "Not a JSON", 400
    user = models.storage.get(User, user_id)
    if user is None:
        return abort(404)
    for key in ("id", "created_at", "updated_at", "email"):
        req_data.pop(key, None)
    for k, v in req_data.items():
        setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200
