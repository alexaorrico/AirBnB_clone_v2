#!/usr/bin/python3
""" API views for User object(s)
Allows routes to list, get, delete, create, and update Users
as requested. """

from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """Returns a list of all Users """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Returns a singular user object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Creates a User"""
    # Check if the Content-Type is application/json
    if request.content_type != 'application/json':
        abort(400,
              description="Invalid Content-Type. Expects 'application/json'")
    # ALWAYS use encryption when setting passwords.
    # You are responsible for your user's data.
    user_data = request.get_json()
    if not user_data:
        abort(400, description="Not a JSON")
    if 'email' not in user_data:
        abort(400, description="Missing email")
    if 'password' not in user_data:
        abort(400, description="Missing password")
    user = User(**user_data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User"""
    # It is generally a bad programming practice to delete a user,
    # any record that references or keys off of a User ID is now
    # invalid. and unaccessible. It's recommended instead to make
    # users 'inactive'. This has been Ben's tips.
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a User"""
    # Check if the Content-Type is application/json
    if request.content_type != 'application/json':
        abort(400,
              description="Invalid Content-Type. Expects 'application/json'")
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user_data = request.get_json()
    if not user_data:
        abort(400, description="Not a JSON")
    for key, value in user_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
