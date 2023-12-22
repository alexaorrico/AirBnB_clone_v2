#!/usr/bin/python3
""" Module used to handle users """
from flask import jsonify, request, abort
from api.v1.views import api_views
from models import storage
from models.user import User


@api_views.route('/users', methods=['GET'])
def get_all_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    for user in users:
        return jsonify([user.to_dict()])


@api_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a User object by its id"""
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(user.to_dict())


@api_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object by its id"""
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({'error': 'Not found'}), 404
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@api_views.route('/users', methods=['POST'])
def create_user():
    """Creates a User"""
    try:
        data = request.get_json()
        if not data or "email" not in data or "password" not in data:
            abort(400, description="Not a JSON or Missing email or password")

        user = User(**data)
        storage.new(user)
        storage.save()

        return jsonify(user.to_dict()), 201
    except Exception:
        return jsonify({"message": "Not a JSON"}), 400


@api_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User object by its id"""
    try:
        data = request.get_json()
        user = storage.get(User, user_id)
        if user is None:
            return jsonify({'error': 'Not found'}), 404
        for key, value in data.items():
            if key not in ["id", "email", "created_at",
                           "updated_at", "password"]:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
    except Exception:
        abort(400, description="Not a JSON or Missing email or password")
