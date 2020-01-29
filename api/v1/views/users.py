#!/usr/bin/python3
"""
    Module of blueprints of flask
"""
from models import storage
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def fetch_all_users():
    """Fetch all states"""
    users_list = []
    users = storage.all("User")
    for user in users.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def fetch_user(user_id):
    """Fetch a state"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("users/<user_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a state"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a state"""
    post_data = request.get_json()
    if post_data is None:
        abort(400, 'Not a JSON')
    if post_data.get('email') is None:
        abort(400, 'Missing email')
    if post_data.get('password') is None:
        abort(400, 'Missing password')
    new_user = User(**post_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a user"""
    attributes_unchanged = ['id', 'created_at', 'updated_at', 'email']
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    put_data = request.get_json()
    if put_data is None:
        abort(400, 'Not a JSON')
    for key, value in put_data.items():
        if key in attributes_unchanged:
            pass
        else:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
