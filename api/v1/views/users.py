#!/usr/bin/python3
"""Create a new view for User object that
handles all default RESTFul API actions:"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Create a new view for User object that handles
    all default RESTFul API actions:"""
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Create a new view for User object that handles
    all default RESTFul API actions:"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Create a new view for User object that
    handles all default RESTFul API actions:"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new view for User object
    that handles all default RESTFul API actions:"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in request.get_json():
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in request.get_json():
        return jsonify({'error': 'Missing password'}), 400
    user = User(**request.get_json())
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Create a new view for User object that
    handles all default RESTFul API actions:"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for attr, val in request.get_json().items():
        if attr not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, attr, val)
    user.save()
    return jsonify(user.to_dict())
