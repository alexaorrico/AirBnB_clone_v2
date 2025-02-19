#!/usr/bin/python3
"""
Module View user
"""
from api.v1.views import app_views
from flask import Flask, abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """List of all users
    """
    all_user = storage.all('User').values()
    if all_user:
        return jsonify([user.to_dict() for user in all_user])
    else:
        return abort(404)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """gets a particular user"""
    user = storage.get('User', user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        return abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a user"""
    user = storage.get('User', user_id)
    if user:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        return abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a user"""
    if request.content_type != 'application/json':
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if 'email' not in data:
        return make_response(jsonify({'error': 'Missing email'}), 400)

    if 'password' not in data:
        return make_response(jsonify({'error': 'Missing password'}), 400)

    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict(), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a User object"""
    user = storage.get('User', user_id)

    data = request.get_json()

    if user is None:
        return abort(404)

    if request.content_type != 'application/json':
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict()), 200
