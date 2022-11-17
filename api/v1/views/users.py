#!/usr/bin/python3
"""Create a new view for State objects that handles all default RESTFul API
actions"""

from api.v1.views import app_views
from flask import request, abort, jsonify
from models.user import User
from models import storage


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def usersWithId(user_id=None):
    """Methods that retrieves all methods for users with id"""
    userId = storage.get(User, user_id)
    if userId is None:
        return abort(404)

    if request.method == 'GET':
        """Retrieves a user of a given user_id"""
        return jsonify(userId.to_dict())

    if request.method == 'DELETE':
        """Deletes a user of a given user_id """
        userId.delete()
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        """Update an user of a given user_id"""
        if request.get_json() is None:
            return abort(400, 'Not a JSON')
        toIgnore = ["id", "email", "created_at", "updated_it"]
        for key, value in request.get_json().items():
            if value not in toIgnore:
                setattr(userId, key, value)
        userId.save()
        return jsonify(userId.to_dict()), 200


@app_views.route('/users', methods=['POST', 'GET'], strict_slashes=False)
def usersNoId():
    """Methods that retrieves all methods for users without id"""
    if request.method == 'POST':
        """Create a new user"""
        if request.get_json() is None:
            return abort(400, 'Not a JSON')
        if request.get_json().get('email') is None:
            return abort(400, 'Missing email')
        if request.get_json().get('password') is None:
            return abort(400, 'Missing password')
        newUser = User(**request.get_json())
        newUser.save()
        return jsonify(newUser.to_dict()), 201

    if request.method == 'GET':
        """Retrieves get method for all users"""
        allUser = storage.all(User)
        user = list(allObject.to_dict() for allObject in allUser.values())
        return jsonify(user)
