#!/usr/bin/python3
"""Users view module."""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, user


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(user.User)
    users_list = []
    for obj in users.values():
        users_list.append(obj.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    obj = storage.get(user.User, user_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    obj = storage.get(user.User, user_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User"""
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in json_data:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in json_data:
        return jsonify({'error': 'Missing password'}), 400
    obj = user.User(**json_data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    obj = storage.get(user.User, user_id)
    if not obj:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in json_data.items():
        if key not in ignore_keys:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
