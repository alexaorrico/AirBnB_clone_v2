#!/usr/bin/python3
"""
Api views for User object
"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """
    Retrieves the list of all User objects:
    """
    users = []
    for user in storage.all("User").values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_user(user_id):
    """
    Retrieves a User object
    """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object
    """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a use object
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    data = request.get_json()
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
    Update a user object
    """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for k, v in request.get_json().items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict())
