#!/usr/bin/python3
"""
Create a new view for User objects
that handles all default RESTFul API actions
"""
from flask import Flask, jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User
import json


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects
    """
    all_users = storage.all(User).values()
    user_list = [user.to_dict() for user in all_users]
    response = make_response(json.dumps(user_list, indent=2))
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    response = make_response(json.dumps(user.to_dict(), indent=2))
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a User"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if "email" not in request.get_json():
        abort(400, description="Missing email")

    if "password" not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    new_user = User(**data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def updata_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    for k, v in data.items():
        if k not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, k, v)

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
