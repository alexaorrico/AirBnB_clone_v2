#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users_get():
    """Retrieves the list of all User"""
    users_list = []
    all_users = storage.all(User)
    for key, value in all_users.items():
        users_list.append(value.to_dict())
    return jsonify(users_list)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def users_post():
    """Creates a User"""
    transform_dict = request.get_json()
    if transform_dict is None:
        abort(400, "Not a JSON")
    if 'email' not in transform_dict.keys():
        abort(400, "Missing email")
    if 'password' not in transform_dict.keys():
        abort(400, "Missing password")
    else:
        new_user = User(**transform_dict)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('users/<user_id>', methods=['GET'], strict_slashes=False)
def users_id_get(user_id):
    """Retrieves a User object and 404 if it's an error"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def users_id_delete(user_id):
    """Deletes a User object and 404 if it's an error"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('users/<user_id>', methods=['PUT'], strict_slashes=False)
def users_id_put(user_id):
    """Updates a User object"""
    ignore_list = ['id', 'created_at', 'updated_at']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    transform_dict = request.get_json()
    if transform_dict is None:
        abort(400, "Not a JSON")
    for key, value in transform_dict.items():
        if key not in ignore_list:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
