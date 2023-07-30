#!/usr/bin/python3
"""The Users Module"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves list of all User objects"""
    a_users = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(a_users)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves User object by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return (jsonify(user.to_dict()), 200)

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes User object by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return (jsonify({}), 200)

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates User object"""
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in data:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in data:
        return make_response(jsonify({"error": "Missing password"}), 400)

    user = User(**data)
    user.save()
    return (jsonify(user.to_dict()), 201)

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates User object by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, val in data.items():
        if key not in ignore_keys:
            setattr(user, key, val)
    storage.save()

    return (jsonify(user.to_dict()), 200)
