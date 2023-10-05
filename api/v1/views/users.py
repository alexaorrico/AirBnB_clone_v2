#!/usr/bin/python3
"""A new view for User objects that handles all default RESTFUL
API actions"""


from flask import Flask, jsonify, request, abort
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_user():
    """Retrives all User objects in the storage
    """
    users = [u.to_dict() for u in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_based_on_id(user_id):
    """Retrives an User object given it's id else return 404
    """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user_object(user_id):
    """Deletes an User object if found otherwise return 404
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user_object():
    """Creates an User object returns the created user object
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates an User object based on the user id
    """
    fetch_user = storage.get(User, user_id)
    if not fetch_user:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    keep = ["id", "created_at", "updated_at", "email"]
    for key, values in data.items():
        if key not in keep:
            setattr(fetch_user, key, values)

    fetch_user.save()
    return jsonify(fetch_user.to_dict()), 200
