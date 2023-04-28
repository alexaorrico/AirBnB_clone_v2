#!/usr/bin/python3
"""User RESTFul API module"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def allUsers():
    """Retrieve all users"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users), 200


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def oneUser(user_id):
    """Retrieves one user with given id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def deleteUser(user_id):
    """Deletes a user with given id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def createUser():
    """Creates and saves a new User"""
    if not request.is_json:
        abort(400, "Not a JSON")
    obj = request.get_json()
    if 'email' not in obj:
        abort(400, "Missing email")
    if 'password' not in obj:
        abort(400, "Missing password")
    user = User(**obj)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def updateUser(user_id):
    """Modifies User data for user with id"""
    if not request.is_json:
        abort(400, "Not a JSON")
    obj = request.get_json()
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    for key, value in obj.items():
        if key not in ('id', 'updated_at', 'created_at', 'email'):
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
