#!/usr/bin/python3
"""Users view for api v1"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_all_users():
    """
        Returns all user objects
    """
    return jsonify([user.to_dict() for user in \
            storage.all(User).values()]), 200


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user_by_id(user_id):
    """
        Returns a user object based on its id. Error if not found
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('/users', strict_slashes=False,
                 methods=['POST'])
def create_user():
    """
        Stores and returns a new user
    """
    user_json = request.get_json(silent=True)
    if not user_json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in user_json:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in user_json:
        return jsonify({'error': 'Missing password'}), 400
    user = User(**user_json)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):
    """
        Updates and returns the information of a given user
    """
    user_json = request.get_json(silent=True)
    if not user_json:
        return jsonify({'error': 'Not a JSON'}), 400
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    for key, val in user_json.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, val)
    user.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_users(user_id):
    """
        Deletes a user with id and returns an empty JSON
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200
