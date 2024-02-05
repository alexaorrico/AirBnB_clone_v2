"""Module providing API endpoints for User resources."""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieve a list of all users."""
    users_list = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users_list)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieve information about a specific user."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a user by its ID."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user."""
    if request.is_json:
        data = request.get_json()
        if 'email' not in data:
            return jsonify({"error": "Missing email"}), 400
        if 'password' not in data:
            return jsonify({"error": "Missing password"}), 400

        user = User(**data)
        storage.new(user)
        storage.save()

        return jsonify(user.to_dict()), 201
    else:
        return jsonify({"error": "Not a JSON"}), 400

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Update a user's information."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
        keys_to_ignore = ['id', 'email', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in keys_to_ignore:
                setattr(user, key, value)
        user.save()

        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"error": "Not a JSON"}), 400
