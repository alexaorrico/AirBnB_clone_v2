#!/usr/bin/python3
"""
This script creates a new view for User object that handles all default RESTFul API actions:

In the file api/v1/views/users.py
You must use to_dict() to retrieve an object into a valid JSON
Update api/v1/views/__init__.py to import this new file
"""
from flask import request, jsonify, abort
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', defaults={'user_id': None}, strict_slashes=False)
@app_views.route('/users/<string:user_id>', strict_slashes=False)
def get_users(user_id):
    """retrieves all users or individual user"""
    users = storage.all(User)
    if user_id is None:
        user_list = [user.to_dict() for user in users.values()]
        return jsonify(user_list)
    else:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """adds a user"""
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in data:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in data:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """updates a user's info"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "Not a JSON"}), 400
    for key in data.keys():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, data[key])
    storage.save()
    return jsonify(user.to_dict()), 200
