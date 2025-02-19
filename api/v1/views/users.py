#!/usr/bin/python3
"""Users route that handles all user RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, make_response, request, jsonify


@app_views.route("/users", strict_slashes=False, methods=["GET"])
@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def user(user_id=None):
    """get users by id"""
    usersList = []
    if user_id is None:
        users = storage.all(User).values()
        for u in users:
            usersList.append(u.to_dict())
        return jsonify(usersList)
    else:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        else:
            return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def delete_user(user_id=None):
    """Delete a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    """Create a user"""
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in data:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in data:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def update_user(user_id=None):
    """ Update user data"""
    data = request.get_json()
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for attr, val in data.items():
        if attr not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, attr, val)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
