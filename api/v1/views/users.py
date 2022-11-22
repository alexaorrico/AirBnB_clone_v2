#!/usr/bin/python3
"""
Module to create view for User objects handling default
RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route("/users/", methods=["GET"])
def users_get():
    """
    Retrieves list of all User objects.
    """
    all_users = storage.all(User)
    user_list = []
    for user in all_users.values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<string:user_id>", methods=["GET"])
def user_id_get(user_id):
    """
    Retrieves an user with a given id
    Raise 404 error if id not linked to any User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", methods=["DELETE"])
def user_id_delete(user_id):
    """
    Deletes an User object with a given id
    Raise 404 error if id not linked to any User object
    Returns and empty dictionary with status code 200
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users/", methods=["POST"])
def user_post():
    """
    Creates an User via POST
    If the HTTP body request is not valid JSON, raise 400 error, Not a JSON
    If the dictionary doesn't contain the key name, raise a 400 error with
    message Missing name
    Returns new User with status code 201
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    new_user = User(**request.get_json())
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/user/<string:user_id>", methods=["PUT"])
def user_put(state_id):
    """
    Updates an User object via PUT
    If the user_id is not linked to any User object, raise 404 error
    If the HTTP body request is not valid JSON, raise a 400 error, Not a JSON
    Update the User object with all key-value pairs of the dictionary
    Ignore keys: id, created_at, updated_at
    """
    user = storage.get(User, state_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    ignore_keys = ["id", "email", "created_at", "updated_at"]
    for key, value in request.get_json().items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
