#!/usr/bin/python3
""" Module for User object view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """ Returns all user objects """
    users_dict_list = [user.to_dict() for
                       user in storage.all("User").values()]
    return jsonify(users_dict_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_id(user_id):
    """ Method retrieves user object with certain id """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Method deletes user object based off of its id """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """ Method creates new user object """
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if body.get("email") is None:
        abort(400, "Missing email")
    if body.get("password") is None:
        abort(400, "Missing password")
    user = User(**body)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """ Method updates a user object based off its id """
    user = storage.get("User", user_id)
    body = request.get_json()
    if not user:
        abort(404)
    if not body:
        abort(400, "Not a JSON")
    for k, v in body.items():
        if k not in ["id", "created_at", "updated_at", "email"]:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict())
