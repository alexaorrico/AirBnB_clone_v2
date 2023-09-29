#!/usr/bin/python3
"""API endpoints for users"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


def get_user_or_abort(user_id):
    """Retrieve a User object by ID or abort with 404 if not found"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return user


def create_user(data):
    """Create a new user in the database."""
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return new_user


def validate_json():
    """Validate that the request data is in JSON format."""
    try:
        return request.get_json()
    except Exception:
        abort(400, "Not a JSON")


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def users():
    """Route for manipulating User objects"""

    if request.method == 'GET':
        # Get a list of all Amenity objects
        users = storage.all(User)
        users_list = [user.to_dict() for user in users.values()]
        return jsonify(users_list)

    if request.method == 'POST':
        # Add a State to the list
        data = validate_json()
        if "email" not in data:
            abort(400, "Missing email")
        if "password" not in data:
            abort(400, "Missing password")
        new_user = create_user(data)
        return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def user_with_id(user_id=None):
    """Route for manipulating a specific City object"""

    user = get_user_or_abort(user_id)

    if request.method == 'GET':
        # Get a specific state by id
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        # Delete a specific state by id
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        # Update a specific state by id
        data = validate_json()
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at", "email"]:
                setattr(user, key, value)
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
