#!/usr/bin/python3
"""User API"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def list_users():
    """list of users"""
    users = storage.all(User)
    return jsonify(
        [user.to_dict() for user in users.values()]
    )


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """Get a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create User"""
    get_json = request.get_json()
    if get_json is None:
        abort(400, 'Not a JSON')
    if get_json.get('email') is None:
        abort(400, 'Missing email')
    if get_json.get('password') is None:
        abort(400, 'Missing password')

    new_user = User(**get_json)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update USer"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    update = request.get_json()

    exx = ['id', 'created_at', 'updated_at', 'email']
    for key, value in update.items():
        if key not in exx:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
