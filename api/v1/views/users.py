#!/usr/bin/python3
"""
View for User objects that will handle all default
RESTful API actions
"""
# Michael Edited 11/22 9:26 AM
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """ Returns a list of all User objects """
    all_users = storage.all(User).values()
    users_list = []
    for user in all_users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route("users/<user_id>", methods=["GET"], strict_slashes=False])
def user_by_id(user_id):
    """
    Returns a user object by specific user ID
    Returns 404 error if user is not found
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("users/<user_id>", methods=["DELETE"], strict_slashes=False])
def delete_user(user_id):
    """
    Deletes a user object by specific user ID
    Returns 404 error if user is not found
    Returns empty dictionary with status code 200
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()

    return jsonify(user.to_dict())