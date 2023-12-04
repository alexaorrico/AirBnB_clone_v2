#!/usr/bin/python3
""" Serves the users """
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=['GET'])
@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=['GET'])
def get_users(user_id=None):
    """
    Returns User objects based on path

    with user_id: Returns a single object
    without user_id: Returns every state
    """
    new_list = []
    key = "User." + str(user_id)
    if user_id is None:
        objs = storage.all(User)
        for key, value in objs.items():
            new_list.append(value.to_dict())
    elif key in storage.all(User).keys():
        return jsonify(storage.all(User)[key].to_dict())
    else:
        abort(404)
    return jsonify(new_list)


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id=None):
    """
    Deletes an User from the database
    """
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    users.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=['POST'])
def post_user():
    """
    Post a User
    """
    if not request.get_json():
        abort(400, "Not a JSON")
    if "email" not in request.get_json():
        abort(400, "Missing email")
    if "password" not in request.get_json():
        abort(400, "Missing password")
    users = User(**request.get_json())
    users.save()
    return jsonify(users.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["PUT"])
def update_user(user_id=None):
    """ Update a user object
    """
    key = "User." + str(user_id)
    if key not in storage.all(User).keys():
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    users = storage.get(User, user_id)
    for key, value in request.get_json().items():
        if key not in ["created_at", "updated_at", "id"]:
            setattr(users, key, value)
    users.save()
    return jsonify(users.to_dict()), 200
