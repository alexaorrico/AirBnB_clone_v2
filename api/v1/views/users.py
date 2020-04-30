#!/usr/bin/python3
"""
"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users_():
    """
    """
    user = storage.all("User")
    users = [i.to_dict() for i in user.values()]
    return (jsonify(users))


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def users_id(user_id=None):
    """
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def user_delete(user_id=None):
    """
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def users_create():
    """
    """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.get_json():
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.get_json():
        return jsonify({"error": "Missing password"}), 400
    instance = User(**request.get_json())
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_update(user_id):
    """
    """
    key = ['id', 'created_at', 'updated_at', 'email']
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for keys, value in request.get_json().items():
        if keys in key:
            pass
        else:
            setattr(user, keys, value)
    user.save()
    return jsonify(user.to_dict()), 200
