#!/usr/bin/python3
"""
Create a new view for User objects - handles all default RESTful API actions
"""

from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """retrieves the list of all User objects"""
    all_users = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(400)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User object"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')

    """Create a new User object with the JSON data"""
    r_user = request.get_json()
    user = User(**r_user)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a User object"""
    if request.get_json():
        new_dict = request.get_json()
        users = storage.all(User).values()
        user_keys = ['id', 'email', 'created_at', 'updated_at']
        for user in users:
            if user.id == user_id:
                for key, value in new_dict.items():
                    if key not in user_keys:
                        setattr(user, key, value)
                storage.save()
                return jsonify(user.to_dict()), 200
        abort(404)
    else:
        abort(400, 'Not a JSON')

    return '', 500
