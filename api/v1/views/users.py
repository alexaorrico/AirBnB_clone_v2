#!/usr/bin/python3
"""Users API routes"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all Users objects"""
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app_views.route(
    '/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a Users object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route(
    '/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User"""
    req_json = request.get_json()
    if req_json is None:
        abort(400, "Not a JSON")
    if 'email' not in req_json:
        abort(400, "Missing email")
    if 'password' not in req_json:
        abort(400, "Missing password")
    user = User(**req_json)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route(
    '/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        abort(400, "Not a JSON")
    ignore_key = ['id', 'email', 'created_at', 'updated_at']
    for key, value in req_json.items():
        if key not in ignore_key:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
