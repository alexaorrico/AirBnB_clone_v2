#!/usr/bin/python3
"""Module for handling users in the API"""

# Import statements
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Get user information for all users"""
    users_list = []
    for user_instance in storage.all("User").values():
        users_list.append(user_instance.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Get user information for the specified user"""
    specified_user = storage.get("User", user_id)
    if specified_user is None:
        abort(404)
    return jsonify(specified_user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a user based on its user_id"""
    specified_user = storage.get("User", user_id)
    if specified_user is None:
        abort(404)
    specified_user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Create a new user"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    new_user = User(**request.get_json())
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Update a user"""
    specified_user = storage.get("User", user_id)
    if specified_user is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attribute, value in request.get_json().items():
        if attribute not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(specified_user, attribute, value)
    specified_user.save()
    return jsonify(specified_user.to_dict())
