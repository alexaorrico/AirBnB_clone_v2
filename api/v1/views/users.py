#!/usr/bin/python3
"""Module with the view for Users objects"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import request, abort, jsonify


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """Return a list of dictionaries of all users"""
    if request.method == 'GET':
        users = []
        for user in storage.all(User).values():
            users.append(user.to_dict())
        return jsonify(users)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    if 'email' not in data.keys():
        return 'Missing email', 400
    if 'password' not in data.keys():
        return 'Missing password', 400
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_id(user_id):
    """Get a user instance from the storage"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return 'Not a JSON', 400
        for k, v in data.items():
            if k != 'id' or k != 'email' or k != 'created_at'\
               or k != 'updated_at':
                setattr(user, k, v)
        storage.save()
        return jsonify(user.to_dict()), 200
