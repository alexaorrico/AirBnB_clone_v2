#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from flasgger.utils import swag_from
from flask import Flask, abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
@swag_from("documentation/user/get.yml", methods=["GET"])
def get_all_users():
    """
    Retrieves the list of all user objects
    """
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route("/users/<string:user_id>", methods=["GET"], strict_slashes=False)
@swag_from("documentation/user/get_id.yml", methods=["GET"])
def get_user_id(user_id):
    """Retrieves a specific user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", methods=["DELETE"], strict_slashes=False)
@swag_from("documentation/user/delete.yml", methods=["DELETE"])
def delete_user(user_id):
    """Deletes a  user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
@swag_from("documentation/user/post_user.yml", methods=["POST"])
def post_user():
    """
    Creates a user
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    body = request.get_json()
    instance = User(**body)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/users/<string:user_id>", methods=["PUT"], strict_slashes=False)
@swag_from("documentation/user/put.yml", methods=["PUT"])
def put_user(user_id):
    """PUTs a  user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "email" not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)

    if "password" not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)

    for key, val in dict(request.get_json()).items():
        setattr(user, key, val)

    storage.save()

    return jsonify(user.to_dict())
