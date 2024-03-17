#!/usr/bin/python3
"""
returns json response for GET, POST, PUT and DELETE
Methods for Users of API
"""
from flask import Flask, jsonify, request, abort, make_response
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Get all User objects"""
    users = [user.to_dict() for user
             in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Get a specific User object"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    response = request.get_json(silent=True)

    if not response:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in response:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in response:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    """Create a new User object"""
    new_user = User(**response)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete an User object"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Update an User object"""
    user = storage.get(User, user_id)
    response = request.get_json(silent=True)
    if not user:
        abort(404)
    if not response:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in response.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return make_response(user.to_dict(), 200)
