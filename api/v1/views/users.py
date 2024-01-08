#!/usr/bin/python3
""" holds class User"""

from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User

@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def get_post_users():
    """Handles GET (retrieve all users) and POST (create new user) requests"""
    if request.method == 'GET':
        # Retrieve all users and return in JSON format
        return jsonify([user.to_dict() for user in storage.all('User').values()])
    elif request.method == 'POST':
        # Create a new user based on POST data in JSON format
        request_data = request.get_json()
        if request_data is None or type(request_data) != dict:
            return jsonify({'error': 'Invalid JSON'}), 400
        elif 'email' not in request_data or 'password' not in request_data:
            return jsonify({'error': 'Missing email or password parameters'}), 400
        new_user = User(**request_data)
        new_user.save()
        return jsonify(new_user.to_dict()), 201

@app_views.route('/users/<string:user_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def get_put_delete_user(user_id):
    """Handles GET (retrieve), PUT (update), and DELETE (remove) requests for a specific user"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)  # Return 404 if user with given ID doesn't exist
    elif request.method == 'GET':
        # Return details of the user in JSON format
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        storage.delete(user)  # Delete the specified user
        storage.save()  # Save changes
        return jsonify({}), 200  # Return empty JSON with 200 status after deletion
    elif request.method == 'PUT':
        # Update attributes of the user based on PUT data in JSON format
        put_data = request.get_json()
        if put_data is None or type(put_data) != dict:
            return jsonify({'error': 'Invalid JSON'}), 400
        for key, value in put_data.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(user, key, value)
        storage.save()  # Save changes
        return jsonify(user.to_dict()), 200  # Return updated user details
