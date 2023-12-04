#!/usr/bin/python3
"""
Module for User objects
"""

import json
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_allusers():
    """
    Get all users
    """

    all_users = storage.all(User).values()
    result = []
    for a_user in all_users:
        result.append(a_user.to_dict())
    return jsonify(result)


@app_views.route("/users/<string:user_id>", methods=['GET'],
                 strict_slashes=False)
def get_userid(user_id):
    """
    Get a user with given id
    """
    result = storage.get(User, user_id)
    if result is None:
        abort(404)
    return jsonify(result.to_dict())


@app_views.route("/users/<string:user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_userid(user_id):
    """
    Delete a user using specified id
    """
    result = storage.get(User, user_id)
    if result is None:
        abort(404)
    storage.delete(result)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'],
                 strict_slashes=False)
def create_user():
    """
    Create new User
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    result = request.get_json()

    if "password" not in result:
        abort(400, description="Missing password")
    if "email" not in result:
        abort(400, description="Missing email")

    item = User(**result)
    storage.new(item)
    storage.save()
    return item.to_dict(), 201


@app_views.route("/users/<user_id>", methods=['PUT', 'GET'],
                 strict_slashes=False)
def update_userid(user_id):
    """
    Updates a User with specified id
    """
    result = storage.get(User, user_id)
    if not result:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")

    json_file = request.get_json()
    for idx, idy in json_file.items():
        if idx != "id" and idx != "updated_at" and idx != "created_at":
            setattr(result, idx, idy)
    storage.save()
    return result.to_dict(), 200
