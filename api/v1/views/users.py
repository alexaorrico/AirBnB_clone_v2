#!/usr/bin/python3
"""route handlers for User object"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.user import User


@app_views.route('/users')
@app_views.route('/users/<user_id>')
def user_index(user_id=None):
    """GET method handler for reading user object"""
    if user_id:
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        return jsonify(user.to_dict())
    else:
        users = storage.all(User).values()
        users = [user.to_dict() for user in users]
        return jsonify(users)


@app_views.route('/users/<user_id>', methods=["DELETE"])
def user_delete(user_id):
    """DELETE method handle for deleting a user object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({})


@app_views.route('/users', methods=['POST'])
def user_post():
    """POST method handler for user object"""
    if not request.is_json:
        return "Not a JSON", 400
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email:
        return "Missing email", 400
    if not password:
        return "Missing password", 400
    user = User()
    user.email = email
    user.password = password
    user.save()
    return jsonify({}), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def user_put(user_id):
    """
    PUT method for updating a user object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if not request.is_json:
        return "Not a JSON", 400
    data = request.get_json()

    for key, value in data.items():
        if key in ('id', 'email', 'created_at', 'updated_at'):
            continue
        else:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict()), 200
