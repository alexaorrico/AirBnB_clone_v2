#!/usr/bin/python3
"""ALX SE Flask Api User Module."""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def get_users():
    """Return list of all users."""
    users = [state.to_dict() for state in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<string:user_id>', strict_slashes=False)
def get_user(user_id: str):
    """Return a user given its id or 404 when not found."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route(
        '/users/<string:user_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_user(user_id: str):
    """Delete a user given its id or 404 when not found."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user."""
    try:
        user_attrs = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if 'name' not in user_attrs:
        abort(400, "Missing name")
    user = User(**user_attrs)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route(
        '/users/<string:user_id>',
        methods=['PUT'],
        strict_slashes=False)
def update_user(user_id: str):
    """Update a user given its id."""
    try:
        user_attrs = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    for key, value in user_attrs.items():
        if key not in ('id', 'updated_at', 'created_at'):
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
