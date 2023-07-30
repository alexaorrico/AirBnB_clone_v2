#!/usr/bin/python3
"""
Handle all the default RESTful api acions
for the user object
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    get user information for all users in a users list
    """
    users = []
    for user in storage.all("User").values():
        users.append(user.to_dict())
    return jsonify(users)

@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """
    get a specific user based on the id provided
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())
