#!/usr/bin/python3

""" View module for user objects that handles all default
RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False,
                 methods=['GET', 'POST'])
def users():
    """Handles GET and POST requests for User objects."""
    if request.method == 'GET':
        # Return a JSON representation of all User objects
        return jsonify([user.to_dict()
                        for user in storage.all(User).values()])

    elif request.method == 'POST':
        # Handle POST request to create a new User object
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        if 'email' not in data:
            return jsonify({"error": "Missing email"}), 400
        if 'password' not in data:
            return jsonify({"error": "Missing password"}), 400

        # Create a new User instance and save it
        new_user = User(**data)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def user_by_id(user_id):
    """Handles GET, DELETE, and PUT requests for a specific User object."""
    # Retrieve the User object with the given ID
    user = storage.get(User, user_id)
    if user is None:
        # Return a 404 error if the user object is not found
        abort(404)

    if request.method == 'GET':
        # Return a JSON representation of the specific User object
        return jsonify(user.to_dict())

    elif request.method == 'DELETE':
        # Handle DELETE request to delete the specific User object
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        # Handle PUT request to update the specific User object
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400

        # Update the User object's attributes based on the request data
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        # Save the updated User object
        storage.save()
        return jsonify(user.to_dict()), 200
