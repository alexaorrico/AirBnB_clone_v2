#!/usr/bin/python3
"""
A view for user that handles all the default RESTFUL api
"""
from flask import make_response, jsonify, abort, request
from models import storage
from models.users import User
from api.v1.views import app_views


@app_views.route('/users', method=['GET'], strict_slashes=False)
def all_users():
    """
    return a list of all users
    """
    u_list = []
    users = storage.all(User)
    for user in useris.values():
        u_list.append(user.to_dict())
    return jsonify(u_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_a_user(user_id):
    """
    returns a user per given id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    user = user.to_dict()
    return jsonify(user)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes a user from the list"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def create_a_user():
    """
    creates a user instance
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)

    user_info = request.get_json()
    newUser = User(**user_info)
    storage.new()
    storage.save(newUser)
    return jsonify(newUser.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    updates an already existing user with new information
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    newUser_info = request.get_json()
    for key, value in newUser_info.items():
        if key not in ['id', 'created_at', 'updated_at']:
            updated_user = setattr(user, key, value)
    storage.save()
    return jsonify(updated_user.to_dict()), 200
