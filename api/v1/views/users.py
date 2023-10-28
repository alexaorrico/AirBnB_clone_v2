#!/usr/bin/python3
"""contains all REST actions for State Objects"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models.user import User
from models import storage

@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def all_users():
    """retrieves a list of all user objects of State"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """retrieves a user objects"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """deletes a user objects"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def new_user():
    """creates a city objects"""
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """updates a user objects"""
    user = storage.get(User, user_id)
    if user:
        if not request.json:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        data = request.get_json()
        ignore_key = ['id', 'email', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_key:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)
