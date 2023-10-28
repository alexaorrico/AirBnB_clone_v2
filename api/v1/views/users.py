#!/usr/bin/python3
"""
users
"""

from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route('/users/', methods=["GET"])
@app_views.route('/users', methods=["GET"])
def users():
    """GET Users"""
    all_users = []
    for value in storage.all(User).values():
        all_users.append(value.to_dict())
    return (jsonify(all_users))


@app_views.route('/users/<string:id>', methods=["GET"])
def user(id):
    """GET User By id"""
    user = storage.get(User, id)
    if user is None:
        abort(404)
    return (jsonify(user.to_dict()))


@app_views.route('/users/<string:id>', methods=["DELETE"])
def remove_User(id):
    """REMOVE User By id"""
    user = storage.get(User, id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return {}, 200


@app_views.route('/users/', methods=["POST"])
def create_User(strict_slashes=False):
    """CREATE User"""
    if request.is_json:
        json_user = request.get_json()
        if json_user.get("email") is None:
            abort(400, description="Missing email")
        if json_user.get("password") is None:
            abort(400, description="Missing password")
        else:
            new = User(**json_user)
            storage.new(new)
            storage.save()
            return new.to_dict(), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/users/<string:id>', methods=["PUT"])
def update_User(id):
    """UPDATE User by id"""
    user = storage.get(User, id)
    if user is None:
        abort(404)
    if request.is_json:
        forbidden = ["id", "created_at", "updated_at", "email"]
        json_user = request.get_json()
        storage.delete(user)
        for k, v in json_user.items():
            if json_user[k] not in forbidden:
                setattr(user, k, v)
        storage.new(user)
        storage.save()
        return user.to_dict(), 200
    else:
        abort(400, description="Not a JSON")
