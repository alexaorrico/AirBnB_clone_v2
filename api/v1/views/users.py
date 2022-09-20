#!/usr/bin/python3
"""objects that handle all default RestFul API actions for Users"""

from flask import abort, request, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models import amenity
from models.user import User


@app_views.route("/users", strict_slashes=False)
def get_user():
    """Retrieves the list of all user objects
    or a specific user"""
    new_list = []
    for user in storage.all(User).values():
        new_list.append(user.to_dict())
    return jsonify(new_list)


@app_views.route("/users/<string:user_id>", strict_slashes=False)
def one_user(user_id):
    """Deletes a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", methods=["DELETE"],
                 strict_slashes=False)
def user_delete(user_id):
    """Method that deletes a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify(({})), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    """Method that creates a user"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Misssing password")
    instance = User(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/users/<string:user_id>", methods=['PUT'],
                 strict_slashes=False)
def user_put(user_id):
    """Method that puts a user"""
    user = storage.get(User, user_id)
    data = request.get_json()
    if not user:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
