#!/usr/bin/python3
"""
View for `User` object that handles all default RESTFul API actions.
"""
from models import storage
from api.v1.views import app_views, User
from flask import abort, jsonify, request
from werkzeug.exceptions import BadRequest


@app_views.route("/users", strict_slashes=False)
def get_user_objects():
    """returns: list of all users"""
    users = storage.all(User)
    user_list = [user.to_dict() for user in users.values()]
    return user_list


@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user_object(user_id):
    """returns: a user object"""
    users = storage.all(User)
    for user in users.values():
        if user.id == user_id:
            return jsonify(user.to_dict())
    # if user not found
    abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user_object(user_id):
    """delete: a user object"""
    users = storage.all(User)
    for user in users.values():
        if user.id == user_id:
            storage.delete(user)
            storage.save()
            return jsonify({}), 200
    # if obj not found
    abort(404)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """create: a new user"""
    try:
        data = request.get_json()
    except BadRequest:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    # create new user
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """updates user with specified id in storage"""
    users = storage.all(User)
    for user in users.values():
        if user.id == user_id:
            try:
                data = request.get_json()
            except BadRequest:
                abort(400, 'Not a JSON')
            # update user obj
            for k, v in data.items():
                if k == 'id' or k == 'email' or k == 'created_at'\
                or k == 'updated_at':
                    continue
                setattr(user, k, v)
                storage.save()
            return jsonify(user.to_dict()), 200
    # object not found
    abort(404)
