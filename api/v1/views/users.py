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


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_user_based_on_id(user_id):
    """ deletes a user object based on id given"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return (jsonify({})), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def add_user_to_db():
    """ adds new user to db """
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    if 'email' not in json_data:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in json_data:
        return jsonify({"error": "Missing password"}), 400
    user = User(**json_data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user_in_db(user_id):
    """ updates a user based on id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    for k, v in json_data.items():
        if k not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict()), 200
