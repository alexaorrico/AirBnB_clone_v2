#!/usr/bin/python3
"""
Create a new view for User object that handles
all default RESTFul API actions
"""
from api.v1.app import app_views
from flask import request, abort
from models.user import User
from models import storage
import json


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ this retrieves the list of all users """
    users = storage.all(User).values()
    list_users = [user.to_dict() for user in users]
    return json.dumps(list_users, indent=2)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def retrieve_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return json.dumps(user.to_dict(), indent=2)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return json.dumps({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates a user"""
    user_data = request.get_json()
    if not user_data:
        abort(400, "Not a JSON")
    elif "email" not in user_data:
        abort(400, "Missing email")
    elif "password" not in user_data:
        abort(400, "Missing password")
    new_user = User(**user_data)
    new_user.save()
    return json.dumps(new_user.to_dict(), indent=2), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ update user info """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user_data = request.get_json()
    if not user_data:
        abort(400, "Not a JSON")
    for key, value in user_data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return json.dumps(user.to_dict(), indent=2), 200
