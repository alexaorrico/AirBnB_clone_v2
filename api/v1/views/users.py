#!/usr/bin/python3
"""
Module that handles the class User in API
"""

from models.user import User
from models import storage
import json
from flask import Flask, jsonify, request, make_response, abort
from api.v1.views import app_views


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id=None):
    """Uses the models class to_dict to retreive all user objects"""
    users = storage.all("User")
    all_users = []

    if user_id is None or user_id is "":
        for user in users.values():
            all_users.append(user.to_dict())
        return jsonify(all_users)
    else:
        for user in users.values():
            if user.id == user_id:
                return jsonify(user.to_dict())
    abort(404)
    return


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Use models class to delete an instace of class User"""
    users = storage.all(User)

    for user in users.values():
        if user.id == user_id:
            user.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def post_user():
    """Method to create a User"""
    payload = request.get_json(silent=True)

    if payload is None:
        abort(400, 'Not a JSON')
    elif 'email' not in payload:
        abort(400, 'Missing email')
    elif 'password' not in payload:
        abort(400, 'Missing password')

    new_user = User(**payload)
    new_user.save()

    return(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Method to update a user object"""
    payload = request.get_json(silent=True)
    users = storage.all(User)

    if payload is None:
        abort(400, 'Not a JSON')

    for user in users.values():
        if user.id == user_id:
            for k, v in payload.items():
                if k != 'created_at' and k != 'updated_at' and k != 'id' \
                   and k != 'email':
                    setattr(user, k, v)
            user.save()
            return(jsonify(user.to_dict()), 200)
    abort(404)
