#!/usr/bin/python3
"""
This is the users page endpoints
"""

from api.v1.views import app_views
from flask import jsonify, request
from werkzeug.exceptions import NotFound
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'])
def fetch_users(user_id=None):
    """Fetches all users objects from the database"""
    users = storage.all(User)
    if user_id:
        for user in users.values():
            user = user.to_dict()
            if user['id'] == user_id:
                return jsonify(user)
        raise NotFound
    return jsonify([object.to_dict() for object in users.values()])


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a user obj using the user id"""
    users = storage.all(User)
    if user_id:
        for user in users.values():
            if user.id == user_id:
                storage.delete(user)
                storage.save()
                return jsonify({}), 200
    raise NotFound


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new user and saves it to the db"""
    user = request.get_json()
    if not user:
        return jsonify(error='Not a JSON'), 400
    if 'email' not in user:
        return jsonify(error='Missing email'), 400
    if 'password' not in user:
        return jsonify(error='Missing password'), 400
    user = User(**user)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """This method updates a user's data"""
    user = storage.get(User, user_id)
    if not user:
        raise NotFound
    new_user = request.get_json()
    if not new_user:
        return jsonify(error='Not a JSON'), 400

    for key, value in new_user.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200