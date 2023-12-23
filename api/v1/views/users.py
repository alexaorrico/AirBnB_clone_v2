#!/usr/bin/python3
"""Create a new view for User object that
handles all default RESTFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_all_users():
    users = storage.all(User).values()
    for user in users:
        return jsonify([user.to_dict()])


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a User object by its id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object by its id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")

    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = storage.get(User, user_id)
    if not data:
        abort(400, description="Not a JSON")
    if user is None:
        abort(404)
        for key, value in data.items():
            if key not in ["id", "email", "created_at",
                           "updated_at"]:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
