#!/usr/bin/python3
"""Handles all RESTFul API actions for User"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Returns a list of all User objects"""
    return [x.to_dict() for x in storage.all(User).values()]


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Returns a User object with a matching id"""
    user = storage.all(User).get(User.__name__ + '.' + user_id, None)
    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes User object with a matching id"""
    user = storage.all(User).get(User.__name__ + '.' + user_id, None)
    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200
