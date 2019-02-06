#!/usr/bin/python3
"""Module to create a new view for State objects"""
from flask import jsonify, Flask, request, abort
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User instances"""
    all_users = storage.all('User')
    my_list = []
    for value in all_users.values():
        my_list.append(value.to_dict())
    return (jsonify(my_list))


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieves the user by ID"""
    user = storage.get('User', user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """Deletes a user by ID"""
    user = storage.get('User', user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Post a User object"""
    data = request.get_json()
    if not data:
        abort(400)
        abort(Response("Not a JSON"))
    if 'email' not in data:
        abort(400)
        abort(Response("Missing name"))
    if 'password' not in data:
        abort(400)
        abort(Response("Missing name"))
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Put a User object"""
    user = storage.get('User', str(user_id))
    if user is None:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    if not data:
        abort(400)
        abort(Response("Not a JSON"))

    # TODO
    # Ignore id, created_at and updated_at
    for k, v in data.items():
        setattr(user, k, v)
        storage.new(user)
        storage.save()
    return jsonify(user.to_dict()), 200
