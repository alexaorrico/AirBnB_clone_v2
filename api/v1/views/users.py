#!/usr/bin/python3
"""User view objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def users():
    """Retrieves the list of all User objects
    """
    return jsonify([user.to_dict()
                   for user in storage.all(User).values()])


@app_views.route('/users/<user_id>', strict_slashes=False)
def user(user_id):
    """Retrieves a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return user.to_dict()


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return {}, 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User
    """
    user = request.get_json()
    if user is None:
        abort(400, "Not a JSON")
    if "email" not in user:
        abort(400, "Missing email")
    if "password" not in user:
        abort(400, "Missing password")
    user = User(**user)
    user.save()
    return user.to_dict(), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user = request.get_json()
    if user is None:
        abort(400, "Not a JSON")
    for key, value in user.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            user[key] = value
    user.save()
    return user.to_dict(), 200
