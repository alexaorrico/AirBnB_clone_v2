#!/usr/bin/python3
"""new view for User objects that handles all
default RestFul API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route(
    "/users", methods=['GET'], strict_slashes=False)
@app_views.route(
    "/users/<user_id>", methods=['GET'], strict_slashes=False)
def user_view(user_id=None):
    """
    Retrieves the list of all User objects
    """
    if user_id:
        my_user = storage.get(User, user_id)
        if my_user is None:
            abort(404)
        return jsonify(my_user.to_dict())
    else:
        users = [val.to_dict() for val in storage.all(User).values()]
        return jsonify(users)


@app_views.route(
    "/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    my_user = storage.get(User, user_id)
    if my_user is None:
        abort(404)
    storage.delete(my_user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def post_user():
    """Creates an User"""
    content = request.get_json()
    if content:
        if content.get('email') is None:
            abort(400, "Missing email")
        if content.get('password') is None:
            abort(400, "Missing password")
        new_user = User(**content)
        new_user.save()
        return jsonify(new_user.to_dict()), 201
    else:
        abort(400, "Not a JSON")


@app_views.route(
    "/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates an User object"""
    my_user = storage.get(User, user_id)
    if my_user is None:
        abort(404)
    else:
        content = request.get_json()
        if content:
            keys_ignored = ['id', 'email', 'created_at', 'updated_at']
            for key, value in content.items():
                if key not in keys_ignored:
                    setattr(my_user, key, value)
            my_user.save()
            return jsonify(my_user.to_dict()), 200
        else:
            abort(400, "Not a JSON")
