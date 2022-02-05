#!/usr/bin/python3
"""view for Amenitites objects"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users/', strict_slashes=False)
def all_users():
    """Retrieves all users"""
    users = storage.all('User')
    new_list = []
    for user in users.values():
        new_list.append(user.to_dict())
    return jsonify(new_list)


@app_views.route('/users/<user_id>', strict_slashes=False)
def user_by_id(user_id):
    """Retrieves a user by a given ID"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route(
    '/users/<user_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/users',
    methods=['POST'],
    strict_slashes=False
    )
def create_user():
    """Creates a User object"""
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request_data:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request_data:
        return jsonify({"error": "Missing password"}), 400
    obj = User(**request_data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route(
    '/users/<user_id>',
    methods=['PUT'],
    strict_slashes=False
    )
def update_user(user_id):
    """Update a User object"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in request_data.items():
        setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict()), 200
