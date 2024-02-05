#!/usr/bin/python3
"""view for city object that handles all default RESTFul API actions"""
from . import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_users():
    """Returns a list of all user objects"""
    users = storage.all(User).values()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Return a dict representation of user object"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user object"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify("{}"), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a user object"""
    if request.json:
        if 'email' not in request.json:
            return jsonify({"error": "Missing email"}), 400
        if 'password' not in request.json:
            return jsonify({"error": "Missing password"}), 400
        data = request.json
        user = User(**data)
        user.save()
        return user.to_dict(), 201
    else:
        return jsonify({"error": "Not a JSON"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """updates user object"""
    user = storage.get(User, user_id)
    if user:
        if request.json:
            for key, value in request.json.items():
                if key not in ['id', 'email', 'created_at', 'updated_at']:
                    setattr(user, key, value)
            return user.to_dict(), 200
        else:
            return jsonify({"error": "Not a JSON"}), 400
    else:
        abort(404)
