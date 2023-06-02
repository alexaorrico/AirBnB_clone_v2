#!/usr/bin/python3
"""
Module that houses the view for User objects
It handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user_list():
    """Retrieves the list of all User objects"""
    users_list = []
    users = storage.all(User).values()
    for user in users:
        users_list.append(user.to_dict())
    return jsonify(users_list), 200


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user_obj(user_id):
    """
    Retrieves an User object

    Args:
        user_id: The id of the user object
    Raises:
        404: if user_id supplied is not linked to any amenity object
    """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"error": "Not found"}), 404


@app_views.route('/users/<user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_users_obj(user_id):
    """
    Deletes an User object

    Args:
        user_id: The id of the user object
    Raises:
        404: if user_id supplied is not linked to any amenity object
    """
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "Not found"}), 404
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates an User object

    Returns:
        The new User with the status code 201
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in data:
        return jsonify({'error': 'Missing name'}), 400
    if 'password' not in data:
        return jsonify({'error': 'Missing password'}), 400
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates an User object

    Args:
        user_id: The id of the user object
    Raises:
        404:
            If user_id supplied is not linked to any user o    bject
            400: If the HTTP body request is not valid JSON
    """
    user = storage.get(User, user_id)
    if not user:
        return jsonify({'error': 'Not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    data.pop('id', None)
    data.pop('created_at', None)
    data.pop('updated_at', None)
    data.pop('email', None)
    for key, value in data.items():
        setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
