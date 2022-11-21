#!/usr/bin/python3
""" Handles Restful API actions for states """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Returns all user objects"""
    allusers = storage.all(User).values()
    users_list = []
    for user in allusers:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Returns all users matching ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes user with the given ID"""

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    post a User object
    """
    if not request.json:
        abort(400, "Not a JSON")
    data = request.json
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    instance = User(**data)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_state(user_id):
    """Updates the user object"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    titles_ignore = ['id', 'email', 'created_at', 'updated_at']

    user_info = request.get_json()
    for key, value in user_info.items():
        if key not in titles_ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
