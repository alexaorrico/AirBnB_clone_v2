#!/usr/bin/python3
"""This module contains the view for User objects"""
from flask import abort, jsonify, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False)
def users():
    objects = storage.all(User)
    """retrieves the list of all User objects"""
    return jsonify([obj.to_dict() for obj in objects.values()])


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user_by_id(user_id):
    """retrieves a User object using it's id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """deletes a User object"""
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """creates a User object"""
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    obj = User(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """updates a User object"""
    obj = storage.get(User, user_id)
    data = request.get_json(silent=True)
    if not obj:
        abort(404)
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if (key not in ['id', 'email', 'created_at', 'updated_at']):
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
