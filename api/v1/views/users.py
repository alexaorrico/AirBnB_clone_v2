#!/usr/bin/python3

"""Module to handle user request Blueprint"""

import hashlib
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """return json array of all users"""
    users = storage.all(User).values()
    return jsonify([val.to_dict() for val in users])


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user"""
    if request.get_json():
        body = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in body:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in body:
        return make_response(jsonify({"error": "Missing password"}), 400)

    new_user = User(**body)
    new_user.save()
    if storage.get(User, new_user.id) is not None:
        return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Method to get a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """delete a single user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """update properties of a single user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.get_json():
        body = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    _exceptions = ["id", "created_at", "updated_at", "email"]
    for k, v in body.items():
        if k not in _exceptions:
            setattr(user, k, v)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
