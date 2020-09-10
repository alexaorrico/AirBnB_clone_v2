#!/usr/bin/python3
"""RESTful API for User object"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.base_model import BaseModel
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """Retrieves the list of all users object """
    users = storage.all('User')
    list_users = []
    for user in users.values():
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    empty_dict = {}
    user.delete()
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a User object """
    my_dict = request.get_json()
    if my_dict is None:
        abort(400, "Not a JSON")
    if "email" not in my_dict.keys():
        abort(400, "Missing email")
    elif "password" not in my_dict.keys():
        abort(400, "Missing password")
    new_user = User(**my_dict)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Update a User object"""
    if user_id:
        my_dict = request.get_json()
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        if my_dict is None:
            abort(400, "Not a JSON")
        for key, value in my_dict.items():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
