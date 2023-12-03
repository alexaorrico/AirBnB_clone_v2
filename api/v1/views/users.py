#!/usr/bin/python3
"""
Module for handling HTTP requests related to User objects
"""

import json
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_all_users():
    """
    Retrieve all users
    """

    all_users = storage.all(User).values()
    res = []
    for a_user in all_users:
        res.append(a_user.to_dict())
    return jsonify(res)


@app_views.route("/users/<string:user_id>", methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """
    Retrieve an user with the given id
    """
    res = storage.get(User, user_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route("/users/<string:user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """
    Delete an user with the given id
    """
    res = storage.get(User, user_id)
    if res is None:
        abort(404)
    storage.delete(res)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'],
                 strict_slashes=False)
def create_new_user():
    """
    Create a new user
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    res = request.get_json()

    if "password" not in res:
        abort(400, description="Missing password")
    if "email" not in res:
        abort(400, description="Missing email")

    item = User(**res)
    storage.new(item)
    storage.save()
    return item.to_dict(), 201


@app_views.route("/users/<user_id>", methods=['PUT', 'GET'],
                 strict_slashes=False)
def update_user_by_id(user_id):
    """
    Update an user with the given id
    """
    res = storage.get(User, user_id)
    if not res:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")

    json_file = request.get_json()
    for idx, idy in json_file.items():
        if idx != "id" and idx != "updated_at" and idx != "created_at":
            setattr(res, idx, idy)
    storage.save()
    return res.to_dict(), 200
