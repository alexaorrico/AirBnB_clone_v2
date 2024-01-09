#!/usr/bin/python3

"""user view."""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User

app = Flask(__name__)


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Get all User objects."""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Get a User object by id."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a User object."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new User."""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if 'email' not in data:
        abort(400, description="Missing email")

    if 'password' not in data:
        abort(400, description="Missing password")

    user = User(**data)
    storage.new(user)
    storage.save()

    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a User object."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ('id', 'email', 'created_at', 'updated_at', 'password'):
            setattr(user, key, value)

    storage.save()

    return jsonify(user.to_dict())
