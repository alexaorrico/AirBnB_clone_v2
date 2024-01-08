#!/usr/bin/python3

from flask import Flask, jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")

    if "email" not in data:
        abort(400, description="Missing email")

    if "password" not in data:
        abort(400, description="Missing password")

    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ["id", "email", "password", "created_at", "updated_at"]:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict()), 200

