#!/usr/bin/python3
"""User view"""


from models.user import User
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage


@app_views.route('/users', methods=["GET", "POST"], strict_slashes=False)
def users():
    """retrieve or create users depending on request method"""
    if request.method == "GET":
        user = storage.all(User).values()
        user_list = []
        for a in user:
            user_list.append(a.to_dict())
        user_list_json = jsonify(user_list)
        return user_list_json
    else:
        user_dict = request.get_json()
        if user_dict is None:
            abort(400, "Not a JSON")
        if "name" not in user_dict:
            abort(400, "Missing name")
        new_user = User(**user_dict)
        new_user.save()
        new_user_json = jsonify(new_user.to_dict())
        return new_user_json, 201


@app_views.route('/users/<user_id>', methods=["GET"],
                 strict_slashes=False)
def users_id(user_id):
    """retrieve user with id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_json = jsonify(user.to_dict())
    return user_json


@app_views.route('/users/<user_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """delete an user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/<user_id>', methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """update an user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_dict = request.get_json()
    if user_dict is None:
        abort(400, "Not a JSON")

    # easier way to update objects
    # AND update all object attributes
    # not just the name

    for k, v in user_dict.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(user, k, v)
    user.save()
    user_json = jsonify(user.to_dict())
    return user_json, 200
