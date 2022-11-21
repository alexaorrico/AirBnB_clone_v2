#!/usr/bin/python3
"""
    Handles API functions for User
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'],
                 strict_slashes=False)
def users():
    """
        Retrieves all users
    """
    if request.method == 'GET':
        user_list = []
        for user in storage.all(User).values():
            user_list.append(user.to_dict())
        return jsonify(user_list)
    if request.method == 'POST':
        info = request.get_json(silent=True)
        if not info:
            abort(400, 'Not a JSON')
        if 'email' not in info:
            abort(400, 'Missing email')
        if 'password' not in info:
            abort(400, 'Missing password')
        new_user = User(**info)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_object(user_id):
    """
    Handles a specified User
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        for review in user.reviews:
            storage.delete(review)
        for place in user.places:
            storage.delete(place)
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        info = request.get_json(silent=True)
        if not info:
            abort(400, 'Not a JSON')
        for key, value in info.items():
            if key in ['id', 'created_at', 'updated_at', 'email']:
                pass
            else:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
