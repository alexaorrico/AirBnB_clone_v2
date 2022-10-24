#!/usr/bin/python3
"""users route"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """Endpoint to retreive all users"""
    all_users = []
    users = storage.all(User)
    for v in users.values():
        all_users.append(v.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves an user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())
