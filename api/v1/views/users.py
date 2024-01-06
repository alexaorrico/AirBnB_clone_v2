#!/usr/bin/python3
"""
View for users that handles all RESTful API actions
"""
from flask import jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Returns a list of all users"""
    users = storage.get(User)
    if users is None:
        abort(404)
    return jsonify(users.to_dict())


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Returns a user"""
    user = storage.get(user, user_id)
    if user is None:
        abort(404)
    user = user.to_dict()
    return jsonify(user)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """"Deletes a user"""
    user = storage.get(user, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def post_user():
    """Adds a new user"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    user = user(**data)
    user.save()
    user = user.to_dict()
    return jsonify(user), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(404, 'Not a JSON')
    for key, value in data.items():
        special_keys = ['id', 'created_at', 'updated_at']
        if key not in special_keys:
            setattr(user, key, value)
        user.save()
        user = user.to_dict()
        return jsonify(user), 200
