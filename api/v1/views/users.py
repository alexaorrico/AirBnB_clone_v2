#!/usr/bin/python3
"""users endpoint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User

@app_views.route('/users', strict_slashes=False)
def get_users():
    """get users"""
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)

@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """get a specific user"""
    user = storage.get(User, user_id)
    if user is not None:
        return jsonify(user.to_dict())
    abort(404)