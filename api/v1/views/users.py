#!/usr/bin/python3
"""
a new view for users objects
that handles all default RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("users", methods=["GET"], strict_slashes=False)
def get_users():
    """ get a list of users """
    users = storage.all(User).values()
    json_users = [user.to_dict() for user in users]
    return jsonify(json_users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ retrieves a amenity object (specified with amenity_id) """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ deletes a user with 'user_id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """ creates a user object """
    user_data = request.get_json()
    if not user_data:
        abort(400, "Not a JSON")
    if 'email' not in user_data:
        abort(400, "Missing email")
    if 'password' not in user_data:
        abort(400, "Missing password")
    new_user = User(**user_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ updates a user object (specified with state_id) """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_data = request.get_json()
    if not user_data:
        abort(400, "Not a JSON")
    for key, value in user_data.items():
        if key not in ('id', 'email', 'created_at', 'updated_at'):
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
