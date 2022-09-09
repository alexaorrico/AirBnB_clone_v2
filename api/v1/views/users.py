#!/usr/bin/python3
"""
User
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """
    Retrieves the list of all User objects
    """
    users = storage.all("User")
    users_list = []
    for user in users.values():
        users_list.append(user.to_dict())
    return(jsonify(users_list))


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def users_id(user_id):
    """
    Retrieves a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return (jsonify(user.to_dict()))


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a User
    """
    if not request.get_json():
        error = {"error": "Not a JSON"}
        return (jsonify(error), 400)
    if "name" not in request.get_json():
        no_name = {"error": "Missing name"}
        return (jsonify(no_name), 400)
    obj_dict = request.get_json()
    user = User(**obj_dict)
    user.save()
    return (jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        error = {"error": "Not a JSON"}
        return (jsonify(error), 400)
    obj_dict = request.get_json()
    user.name = obj_dict["name"]
    user.save()
    return (jsonify(user.to_dict()), 200)
