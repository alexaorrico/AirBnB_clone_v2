#!/usr/bin/python3
""" View for Users """

from flask import jsonify, request, abort
from models import User
from api.v1.views import app_views


@app_views.route('/users',
                 methods=['GET'],
                 strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = User.query.all()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app_views.route('/users/<user_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a specific User object by its ID"""
    user = User.query.get(user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a specific User object by its ID"""
    user = User.query.get(user_id)
    if not user:
        abort(404)
    user.delete()
    return jsonify({}), 200


@app_views.route('/users',
                 methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Creates a new User object"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a specific User object by its ID"""
    user = User.query.get(user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    keys_to_ignore = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in keys_to_ignore:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
