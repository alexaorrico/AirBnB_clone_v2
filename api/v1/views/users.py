#!/usr/bin/python3
"""module for api configuration"""

from flask import Flask, jsonify, request
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_list_od_users(user_id=None):
    """returns list of all users"""
    if user_id is None:
        users = [user.to_dict() for user in storage.all(User).values()]
        return jsonify(users)
    else:
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        else:
            return jsonify(user.to_dict())
