#!/usr/bin/python3
"""User view"""

from flask import Flask, abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'],
                 strict_slashes=False)
@app_views.route("/users/<user_id>", methods=['GET'],
                 strict_slashes=False)
def get_users(user_id=None):
    """
    get all users
    or get any user with the user_id that is passed
    """
    new_list = []
    key = "User." + str(user_id)
    if user_id is None:
        objs = storage.all(User)
        for key, value in objs.items():
            new_list.append(value.to_dict())
    elif key in storage.all(User).keys():
        return jsonify(storage.all(User)[key].to_dict())
    else:
        abort(404)
    return jsonify(new_list)


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id=None):
    """
    delete any user that the user_id is passed
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'],
                 strict_slashes=False)
def create_user():
    """
    create a new user
    """
    if not request.get_json():
        abort(400, "Not a JSON")
    if "email" not in request.get_json():
        abort(400, "Missing email")
    if "password" not in request.get_json():
        abort(400, "Missing Password")
    user = User(**request.get_json())
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id=None):
    """
    update any user the id is passed
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    key = "User." + str(user_id)
    if key not in storage.all(User).keys():
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "password" not in request.json():
        abort(400, "Missing password")
    for key, value in request.get_json().items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
