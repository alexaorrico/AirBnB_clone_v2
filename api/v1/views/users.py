#!/usr/bin/python3

from flask import Flask, jsonify, abort, request
from modles import storage
from models.user import User
from api.vi.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retreive the list of all users objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slasheds=False)
def get_user(user_id):
    """Retrieve the specific user object by Id"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slasheds=False)
def delete_user(user_id):
    """Delete a User object by ID"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slasheds=False)
def create_user():
    """Create a new user object"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slasheds=False)
def update_user(user_id):
    """Update a User Object by ID"""
    if user:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a Json"}), 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, value)


        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)
